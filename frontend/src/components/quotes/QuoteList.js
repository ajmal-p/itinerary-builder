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
import { Add, PictureAsPdf } from '@mui/icons-material';
import { Link as RouterLink } from 'react-router-dom';
import { useApp } from '../../store/AppContext';
import { quoteService } from '../../services';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const QuoteList = () => {
  const { quotes, fetchQuotes, loading } = useApp();
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchQuotes();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleExportPDF = async (quoteId) => {
    try {
      const response = await quoteService.exportPDF(quoteId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `quote_${quoteId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError(err.message);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      draft: 'default',
      sent: 'info',
      accepted: 'success',
      rejected: 'error',
    };
    return colors[status] || 'default';
  };

  if (loading) return <Loading />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Quotes</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Add />}
          component={RouterLink}
          to="/quotes/new"
        >
          Create Quote
        </Button>
      </Box>

      <ErrorMessage message={error} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Quote ID</TableCell>
              <TableCell>Enquiry ID</TableCell>
              <TableCell>Itinerary ID</TableCell>
              <TableCell>Base Price</TableCell>
              <TableCell>Markup %</TableCell>
              <TableCell>Total Price</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {quotes.map((quote) => (
              <TableRow key={quote.id}>
                <TableCell>{quote.id}</TableCell>
                <TableCell>{quote.enquiry_id}</TableCell>
                <TableCell>{quote.itinerary_id}</TableCell>
                <TableCell>${quote.base_price?.toFixed(2)}</TableCell>
                <TableCell>{quote.markup_percentage}%</TableCell>
                <TableCell>${quote.total_price?.toFixed(2)}</TableCell>
                <TableCell>
                  <Chip
                    label={quote.status}
                    color={getStatusColor(quote.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton
                    onClick={() => handleExportPDF(quote.id)}
                    color="primary"
                    title="Export PDF"
                  >
                    <PictureAsPdf />
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

export default QuoteList;
