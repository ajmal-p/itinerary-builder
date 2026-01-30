import React from 'react';
import { Container, Typography, Paper, Box, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Home = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h3" gutterBottom>
          Welcome to Itinerary Builder
        </Typography>
        <Typography variant="body1" paragraph>
          A comprehensive full-stack application for building and managing travel itineraries.
        </Typography>

        <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="h5" gutterBottom>
            Quick Start
          </Typography>
          
          <Box>
            <Typography variant="h6" gutterBottom>
              1. Manage Your Resources
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button variant="outlined" component={RouterLink} to="/hotels">
                Hotels
              </Button>
              <Button variant="outlined" component={RouterLink} to="/activities">
                Activities
              </Button>
              <Button variant="outlined" component={RouterLink} to="/transfers">
                Transfers
              </Button>
              <Button variant="outlined" component={RouterLink} to="/meals">
                Meals
              </Button>
            </Box>
          </Box>

          <Box>
            <Typography variant="h6" gutterBottom>
              2. Manage Customers & Enquiries
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button variant="outlined" component={RouterLink} to="/customers">
                Customers
              </Button>
              <Button variant="outlined" component={RouterLink} to="/enquiries">
                Enquiries
              </Button>
            </Box>
          </Box>

          <Box>
            <Typography variant="h6" gutterBottom>
              3. Build Itineraries & Generate Quotes
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button variant="contained" component={RouterLink} to="/itineraries">
                Itineraries
              </Button>
              <Button variant="contained" component={RouterLink} to="/quotes">
                Quotes
              </Button>
            </Box>
          </Box>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Features
          </Typography>
          <Typography component="ul">
            <li>Complete CRUD operations for Hotels, Activities, Transfers, and Meals</li>
            <li>Customer and Enquiry management</li>
            <li>Interactive Itinerary Builder</li>
            <li>Quote generation with pricing breakdown</li>
            <li>PDF export for quotes</li>
            <li>Automatic pricing calculations</li>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Home;
