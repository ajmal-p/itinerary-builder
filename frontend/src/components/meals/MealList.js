import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Box,
} from '@mui/material';
import { Edit, Delete, Add } from '@mui/icons-material';
import { useApp } from '../../store/AppContext';
import { mealService } from '../../services';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const MealList = () => {
  const { meals, fetchMeals, setMeals, loading } = useApp();
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMeals();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this meal?')) {
      try {
        await mealService.delete(id);
        setMeals(meals.filter((m) => m.id !== id));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Meals</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          disabled
        >
          Add Meal
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>Cuisine</TableCell>
              <TableCell>Venue</TableCell>
              <TableCell>Pricing</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {meals.map((meal) => (
              <TableRow key={meal.id}>
                <TableCell>{meal.meal_type}</TableCell>
                <TableCell>{meal.cuisine}</TableCell>
                <TableCell>{meal.venue}</TableCell>
                <TableCell>${meal.pricing}</TableCell>
                <TableCell>
                  <IconButton color="primary" disabled>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(meal.id)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default MealList;
