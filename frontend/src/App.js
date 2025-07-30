import React from "react";
import "./App.css";
import { portfolioData } from "./data/mock";

function App() {
  const { hero, projects, contact } = portfolioData;

  return (
    <div className="App">
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        {/* Hero Section */}
        <header style={{ textAlign: 'center', marginBottom: '50px' }}>
          <img 
            src={hero.image} 
            alt="Jane Larsen" 
            style={{ width: '200px', height: '200px', borderRadius: '50%', objectFit: 'cover' }}
          />
          <h1 style={{ fontSize: '3rem', margin: '20px 0' }}>{hero.name}</h1>
          <h2 style={{ fontSize: '1.5rem', color: '#666' }}>{hero.title}</h2>
          <p style={{ fontSize: '1rem', maxWidth: '600px', margin: '0 auto' }}>
            {hero.description}
          </p>
        </header>

        {/* Projects Section */}
        <section style={{ marginBottom: '50px' }}>
          <h2 style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '30px' }}>
            Portfolio Projects
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
            {projects.map((project) => (
              <div key={project.id} style={{ 
                border: '1px solid #ddd', 
                borderRadius: '8px', 
                padding: '20px',
                backgroundColor: '#f9f9f9'
              }}>
                <img 
                  src={project.image} 
                  alt={project.title}
                  style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '4px' }}
                />
                <h3 style={{ margin: '15px 0 10px 0' }}>{project.title}</h3>
                <p style={{ color: '#666', fontSize: '0.9rem' }}>{project.description}</p>
                <div style={{ marginTop: '10px' }}>
                  {project.tools.map((tool, index) => (
                    <span key={index} style={{ 
                      display: 'inline-block',
                      backgroundColor: '#e0e0e0',
                      padding: '4px 8px',
                      margin: '2px',
                      borderRadius: '4px',
                      fontSize: '0.8rem'
                    }}>
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Contact Section */}
        <section style={{ textAlign: 'center', backgroundColor: '#f0f0f0', padding: '40px', borderRadius: '8px' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '20px' }}>Get In Touch</h2>
          <p style={{ fontSize: '1.1rem', marginBottom: '20px' }}>
            Ready to streamline your content workflow with AI-powered automation?
          </p>
          <div style={{ fontSize: '1.1rem' }}>
            <p><strong>Email:</strong> {contact.email}</p>
            <p><strong>Phone:</strong> {contact.phone}</p>
            <p><strong>Location:</strong> {contact.location}</p>
          </div>
        </section>

        {/* Footer */}
        <footer style={{ textAlign: 'center', marginTop: '50px', color: '#666' }}>
          <p>© 2025 Jane Larsen. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
