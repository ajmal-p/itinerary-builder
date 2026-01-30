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
import { activityService } from '../../services';
import ActivityForm from './ActivityForm';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const ActivityList = () => {
  const { activities, fetchActivities, setActivities, loading } = useApp();
  const [openForm, setOpenForm] = useState(false);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchActivities();
  }, []);

  const handleAdd = () => {
    setSelectedActivity(null);
    setOpenForm(true);
  };

  const handleEdit = (activity) => {
    setSelectedActivity(activity);
    setOpenForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this activity?')) {
      try {
        await activityService.delete(id);
        setActivities(activities.filter((a) => a.id !== id));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const handleFormClose = () => {
    setOpenForm(false);
    setSelectedActivity(null);
  };

  const handleFormSubmit = async (data) => {
    try {
      if (selectedActivity) {
        const response = await activityService.update(selectedActivity.id, data);
        setActivities(activities.map((a) => (a.id === selectedActivity.id ? response.data : a)));
      } else {
        const response = await activityService.create(data);
        setActivities([...activities, response.data]);
      }
      handleFormClose();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Activities</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          onClick={handleAdd}
        >
          Add Activity
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Duration</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Pricing</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {activities.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>{activity.name}</TableCell>
                <TableCell>{activity.location}</TableCell>
                <TableCell>{activity.duration}</TableCell>
                <TableCell>{activity.category}</TableCell>
                <TableCell>${activity.pricing}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleEdit(activity)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(activity.id)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <ActivityForm
        open={openForm}
        activity={selectedActivity}
        onClose={handleFormClose}
        onSubmit={handleFormSubmit}
      />
    </Container>
  );
};

export default ActivityList;
