import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Grid,
  Chip,
  Box,
} from '@mui/material';
import { Add, Edit } from '@mui/icons-material';
import { Link as RouterLink } from 'react-router-dom';
import { useApp } from '../../store/AppContext';
import { itineraryService } from '../../services';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const ItineraryList = () => {
  const { itineraries, fetchItineraries, loading } = useApp();
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchItineraries();
  }, []);

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Itineraries</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          component={RouterLink}
          to="/itineraries/new"
        >
          Create Itinerary
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <Grid container spacing={3}>
        {itineraries.map((itinerary) => (
          <Grid item xs={12} sm={6} md={4} key={itinerary.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {itinerary.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {itinerary.description}
                </Typography>
                <Box mt={2}>
                  <Chip
                    label={`Total: $${itinerary.total_price}`}
                    color="primary"
                    size="small"
                  />
                  <Chip
                    label={`${itinerary.items?.length || 0} items`}
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  component={RouterLink}
                  to={`/itineraries/${itinerary.id}`}
                  startIcon={<Edit />}
                >
                  View/Edit
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default ItineraryList;
