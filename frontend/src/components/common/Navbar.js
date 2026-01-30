import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Itinerary Builder v2.0
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" component={RouterLink} to="/">
            Home
          </Button>
          <Button color="inherit" component={RouterLink} to="/hotels">
            Hotels
          </Button>
          <Button color="inherit" component={RouterLink} to="/activities">
            Activities
          </Button>
          <Button color="inherit" component={RouterLink} to="/transfers">
            Transfers
          </Button>
          <Button color="inherit" component={RouterLink} to="/meals">
            Meals
          </Button>
          <Button color="inherit" component={RouterLink} to="/customers">
            Customers
          </Button>
          <Button color="inherit" component={RouterLink} to="/enquiries">
            Enquiries
          </Button>
          <Button color="inherit" component={RouterLink} to="/itineraries">
            Itineraries
          </Button>
          <Button color="inherit" component={RouterLink} to="/quotes">
            Quotes
          </Button>
          <Button color="inherit" component={RouterLink} to="/currencies">
            Currencies
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
