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
  Chip,
} from '@mui/material';
import { Edit, Delete, Add } from '@mui/icons-material';
import { useApp } from '../../store/AppContext';
import { enquiryService } from '../../services';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const EnquiryList = () => {
  const { enquiries, fetchEnquiries, setEnquiries, loading } = useApp();
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEnquiries();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this enquiry?')) {
      try {
        await enquiryService.delete(id);
        setEnquiries(enquiries.filter((e) => e.id !== id));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'info',
      in_progress: 'warning',
      converted: 'success',
      closed: 'default',
    };
    return colors[status] || 'default';
  };

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Enquiries</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          disabled
        >
          Add Enquiry
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Customer ID</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Notes</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {enquiries.map((enquiry) => (
              <TableRow key={enquiry.id}>
                <TableCell>{enquiry.id}</TableCell>
                <TableCell>{enquiry.customer_id}</TableCell>
                <TableCell>
                  <Chip
                    label={enquiry.status}
                    color={getStatusColor(enquiry.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{enquiry.notes}</TableCell>
                <TableCell>
                  <IconButton color="primary" disabled>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(enquiry.id)} color="error">
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

export default EnquiryList;
