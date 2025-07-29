from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Contact Form Models
class ContactInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    subject: str
    message: str
    status: str = "new"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContactInquiryCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactInquiryResponse(BaseModel):
    success: bool
    message: str
    id: str

# Project Models
class ProjectDetails(BaseModel):
    overview: str
    challenges: str
    solution: str
    results: str
    features: List[str]

class Project(BaseModel):
    id: int
    title: str
    description: str
    image: str
    category: str
    tools: List[str]
    details: ProjectDetails
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(BaseModel):
    title: str
    description: str
    image: str
    category: str
    tools: List[str]
    details: ProjectDetails

# Stats Model
class PortfolioStats(BaseModel):
    projects_completed: str
    happy_clients: str
    average_time_saved: str
    average_growth: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Contact Form Endpoints
@api_router.post("/contact", response_model=ContactInquiryResponse)
async def submit_contact_form(inquiry: ContactInquiryCreate):
    try:
        # Create contact inquiry object
        contact_data = inquiry.dict()
        contact_obj = ContactInquiry(**contact_data)
        
        # Insert into database
        result = await db.contact_inquiries.insert_one(contact_obj.dict())
        
        if result.inserted_id:
            return ContactInquiryResponse(
                success=True,
                message="Thank you for reaching out. I'll get back to you within 24 hours.",
                id=contact_obj.id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save contact inquiry")
            
    except Exception as e:
        logger.error(f"Error submitting contact form: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/contact", response_model=List[ContactInquiry])
async def get_contact_inquiries():
    try:
        inquiries = await db.contact_inquiries.find().sort("created_at", -1).to_list(100)
        return [ContactInquiry(**inquiry) for inquiry in inquiries]
    except Exception as e:
        logger.error(f"Error fetching contact inquiries: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Project Endpoints
@api_router.get("/projects", response_model=List[Project])
async def get_projects(category: Optional[str] = None):
    try:
        filter_query = {"is_active": True}
        if category and category.lower() != "all":
            filter_query["category"] = category
            
        projects = await db.projects.find(filter_query).sort("id", 1).to_list(100)
        return [Project(**project) for project in projects]
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: int):
    try:
        project = await db.projects.find_one({"id": project_id, "is_active": True})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return Project(**project)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Portfolio Stats Endpoint
@api_router.get("/stats", response_model=PortfolioStats)
async def get_portfolio_stats():
    try:
        # Get actual counts from database
        total_projects = await db.projects.count_documents({"is_active": True})
        total_inquiries = await db.contact_inquiries.count_documents({})
        
        # Return stats (mixing real data with marketing numbers)
        return PortfolioStats(
            projects_completed=f"{max(total_projects, 500)}+",
            happy_clients="50+",
            average_time_saved="70%", 
            average_growth="300%"
        )
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
