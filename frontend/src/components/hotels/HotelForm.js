import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Grid,
} from '@mui/material';

const HotelForm = ({ open, hotel, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    star_rating: '',
    pricing: '',
    description: '',
    amenities: [],
    images: [],
    room_types: {},
  });

  useEffect(() => {
    if (hotel) {
      setFormData(hotel);
    } else {
      setFormData({
        name: '',
        location: '',
        star_rating: '',
        pricing: '',
        description: '',
        amenities: [],
        images: [],
        room_types: {},
      });
    }
  }, [hotel]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const submitData = {
      ...formData,
      star_rating: formData.star_rating ? parseInt(formData.star_rating) : null,
      pricing: formData.pricing ? parseFloat(formData.pricing) : null,
    };
    onSubmit(submitData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>{hotel ? 'Edit Hotel' : 'Add Hotel'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                name="name"
                label="Name"
                value={formData.name}
                onChange={handleChange}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="location"
                label="Location"
                value={formData.location}
                onChange={handleChange}
                fullWidth
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="star_rating"
                label="Star Rating"
                type="number"
                value={formData.star_rating}
                onChange={handleChange}
                fullWidth
                inputProps={{ min: 1, max: 5 }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="pricing"
                label="Pricing"
                type="number"
                value={formData.pricing}
                onChange={handleChange}
                fullWidth
                inputProps={{ min: 0, step: 0.01 }}
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
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" color="primary">
            {hotel ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default HotelForm;
