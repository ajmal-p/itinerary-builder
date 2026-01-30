import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  TextField,
  Grid,
  Paper,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Divider,
} from '@mui/material';
import { Add, Delete, Save } from '@mui/icons-material';
import { useApp } from '../../store/AppContext';
import { itineraryService } from '../../services';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const ItineraryBuilder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { hotels, activities, transfers, meals, fetchHotels, fetchActivities, fetchTransfers, fetchMeals } = useApp();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
  });
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({
    day_number: 1,
    item_type: 'hotel',
    item_order: 0,
    hotel_id: null,
    activity_id: null,
    transfer_id: null,
    meal_id: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadItinerary = useCallback(async () => {
    try {
      setLoading(true);
      const response = await itineraryService.getById(id);
      setFormData({
        name: response.data.name,
        description: response.data.description || '',
        start_date: response.data.start_date || '',
        end_date: response.data.end_date || '',
      });
      setItems(response.data.items || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchHotels();
    fetchActivities();
    fetchTransfers();
    fetchMeals();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (id && id !== 'new') {
      loadItinerary();
    }
  }, [id, loadItinerary]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleNewItemChange = (e) => {
    const { name, value } = e.target;
    setNewItem({ ...newItem, [name]: value });
  };

  const handleAddItem = () => {
    setItems([...items, { ...newItem, id: Date.now() }]);
    setNewItem({
      day_number: newItem.day_number,
      item_type: 'hotel',
      item_order: items.filter(i => i.day_number === newItem.day_number).length,
      hotel_id: null,
      activity_id: null,
      transfer_id: null,
      meal_id: null,
    });
  };

  const handleRemoveItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      const data = {
        ...formData,
        items: items.map(item => ({
          day_number: parseInt(item.day_number),
          item_type: item.item_type,
          item_order: parseInt(item.item_order),
          hotel_id: item.hotel_id ? parseInt(item.hotel_id) : null,
          activity_id: item.activity_id ? parseInt(item.activity_id) : null,
          transfer_id: item.transfer_id ? parseInt(item.transfer_id) : null,
          meal_id: item.meal_id ? parseInt(item.meal_id) : null,
        })),
      };

      if (id && id !== 'new') {
        await itineraryService.update(id, data);
      } else {
        await itineraryService.create(data);
      }
      navigate('/itineraries');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getItemOptions = () => {
    switch (newItem.item_type) {
      case 'hotel':
        return hotels;
      case 'activity':
        return activities;
      case 'transfer':
        return transfers;
      case 'meal':
        return meals;
      default:
        return [];
    }
  };

  const getItemIdField = () => {
    return `${newItem.item_type}_id`;
  };

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        {id && id !== 'new' ? 'Edit Itinerary' : 'Create Itinerary'}
      </Typography>

      <ErrorMessage message={error} />

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              name="name"
              label="Itinerary Name"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              name="start_date"
              label="Start Date"
              type="date"
              value={formData.start_date}
              onChange={handleChange}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              name="end_date"
              label="End Date"
              type="date"
              value={formData.end_date}
              onChange={handleChange}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              name="description"
              label="Description"
              value={formData.description}
              onChange={handleChange}
              fullWidth
              multiline
              rows={3}
            />
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Add Items to Itinerary
        </Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={2}>
            <TextField
              name="day_number"
              label="Day"
              type="number"
              value={newItem.day_number}
              onChange={handleNewItemChange}
              fullWidth
              inputProps={{ min: 1 }}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                name="item_type"
                value={newItem.item_type}
                onChange={handleNewItemChange}
                label="Type"
              >
                <MenuItem value="hotel">Hotel</MenuItem>
                <MenuItem value="activity">Activity</MenuItem>
                <MenuItem value="transfer">Transfer</MenuItem>
                <MenuItem value="meal">Meal</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={5}>
            <FormControl fullWidth>
              <InputLabel>Select Item</InputLabel>
              <Select
                name={getItemIdField()}
                value={newItem[getItemIdField()] || ''}
                onChange={handleNewItemChange}
                label="Select Item"
              >
                {getItemOptions().map((option) => (
                  <MenuItem key={option.id} value={option.id}>
                    {option.name} {option.pricing && `- $${option.pricing}`}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={2}>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={handleAddItem}
              fullWidth
            >
              Add
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Itinerary Items
        </Typography>
        <List>
          {items.map((item, index) => (
            <React.Fragment key={index}>
              <ListItem
                secondaryAction={
                  <IconButton edge="end" onClick={() => handleRemoveItem(index)} color="error">
                    <Delete />
                  </IconButton>
                }
              >
                <ListItemText
                  primary={`Day ${item.day_number} - ${item.item_type}`}
                  secondary={`ID: ${item[`${item.item_type}_id`]}`}
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
        </List>
      </Paper>

      <Box display="flex" justifyContent="flex-end" gap={2}>
        <Button variant="outlined" onClick={() => navigate('/itineraries')}>
          Cancel
        </Button>
        <Button
          variant="contained"
          startIcon={<Save />}
          onClick={handleSave}
        >
          Save Itinerary
        </Button>
      </Box>
    </Container>
  );
};

export default ItineraryBuilder;
