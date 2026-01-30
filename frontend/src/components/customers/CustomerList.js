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
import { customerService } from '../../services';
import CustomerForm from './CustomerForm';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const CustomerList = () => {
  const { customers, fetchCustomers, setCustomers, loading } = useApp();
  const [openForm, setOpenForm] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleAdd = () => {
    setSelectedCustomer(null);
    setOpenForm(true);
  };

  const handleEdit = (customer) => {
    setSelectedCustomer(customer);
    setOpenForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      try {
        await customerService.delete(id);
        setCustomers(customers.filter((c) => c.id !== id));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const handleFormClose = () => {
    setOpenForm(false);
    setSelectedCustomer(null);
  };

  const handleFormSubmit = async (data) => {
    try {
      if (selectedCustomer) {
        const response = await customerService.update(selectedCustomer.id, data);
        setCustomers(customers.map((c) => (c.id === selectedCustomer.id ? response.data : c)));
      } else {
        const response = await customerService.create(data);
        setCustomers([...customers, response.data]);
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
        <Typography variant="h4">Customers</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          onClick={handleAdd}
        >
          Add Customer
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {customers.map((customer) => (
              <TableRow key={customer.id}>
                <TableCell>{customer.name}</TableCell>
                <TableCell>{customer.email}</TableCell>
                <TableCell>{customer.phone}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleEdit(customer)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(customer.id)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <CustomerForm
        open={openForm}
        customer={selectedCustomer}
        onClose={handleFormClose}
        onSubmit={handleFormSubmit}
      />
    </Container>
  );
};

export default CustomerList;
