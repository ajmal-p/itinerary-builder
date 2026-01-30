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
import { hotelService } from '../../services';
import HotelForm from './HotelForm';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const HotelList = () => {
  const { hotels, fetchHotels, setHotels, loading } = useApp();
  const [openForm, setOpenForm] = useState(false);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHotels();
  }, []);

  const handleAdd = () => {
    setSelectedHotel(null);
    setOpenForm(true);
  };

  const handleEdit = (hotel) => {
    setSelectedHotel(hotel);
    setOpenForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this hotel?')) {
      try {
        await hotelService.delete(id);
        setHotels(hotels.filter((h) => h.id !== id));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const handleFormClose = () => {
    setOpenForm(false);
    setSelectedHotel(null);
  };

  const handleFormSubmit = async (data) => {
    try {
      if (selectedHotel) {
        const response = await hotelService.update(selectedHotel.id, data);
        setHotels(hotels.map((h) => (h.id === selectedHotel.id ? response.data : h)));
      } else {
        const response = await hotelService.create(data);
        setHotels([...hotels, response.data]);
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
        <Typography variant="h4">Hotels</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          onClick={handleAdd}
        >
          Add Hotel
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Star Rating</TableCell>
              <TableCell>Pricing</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {hotels.map((hotel) => (
              <TableRow key={hotel.id}>
                <TableCell>{hotel.name}</TableCell>
                <TableCell>{hotel.location}</TableCell>
                <TableCell>{hotel.star_rating}</TableCell>
                <TableCell>${hotel.pricing}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleEdit(hotel)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(hotel.id)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <HotelForm
        open={openForm}
        hotel={selectedHotel}
        onClose={handleFormClose}
        onSubmit={handleFormSubmit}
      />
    </Container>
  );
};

export default HotelList;
