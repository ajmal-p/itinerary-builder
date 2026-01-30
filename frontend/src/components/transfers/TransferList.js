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
import { transferService } from '../../services';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const TransferList = () => {
  const { transfers, fetchTransfers, setTransfers, loading } = useApp();
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTransfers();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this transfer?')) {
      try {
        await transferService.delete(id);
        setTransfers(transfers.filter((t) => t.id !== id));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Transfers</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          disabled
        >
          Add Transfer
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>Vehicle</TableCell>
              <TableCell>Capacity</TableCell>
              <TableCell>Pickup</TableCell>
              <TableCell>Dropoff</TableCell>
              <TableCell>Pricing</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transfers.map((transfer) => (
              <TableRow key={transfer.id}>
                <TableCell>{transfer.transfer_type}</TableCell>
                <TableCell>{transfer.vehicle_type}</TableCell>
                <TableCell>{transfer.capacity}</TableCell>
                <TableCell>{transfer.pickup_point}</TableCell>
                <TableCell>{transfer.dropoff_point}</TableCell>
                <TableCell>${transfer.pricing}</TableCell>
                <TableCell>
                  <IconButton color="primary" disabled>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(transfer.id)} color="error">
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

export default TransferList;
