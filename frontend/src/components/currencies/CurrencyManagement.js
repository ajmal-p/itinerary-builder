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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Switch,
  FormControlLabel,
} from '@mui/material';
import { Edit, Delete, Add, Refresh, Star } from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const CurrencyManagement = () => {
  const [currencies, setCurrencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openForm, setOpenForm] = useState(false);
  const [selectedCurrency, setSelectedCurrency] = useState(null);
  const [formData, setFormData] = useState({
    code: '',
    name: '',
    symbol: '',
    is_base_currency: false,
    is_active: true,
  });

  useEffect(() => {
    fetchCurrencies();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchCurrencies = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/currencies/`);
      setCurrencies(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setSelectedCurrency(null);
    setFormData({
      code: '',
      name: '',
      symbol: '',
      is_base_currency: false,
      is_active: true,
    });
    setOpenForm(true);
  };

  const handleEdit = (currency) => {
    setSelectedCurrency(currency);
    setFormData({
      code: currency.code,
      name: currency.name,
      symbol: currency.symbol || '',
      is_base_currency: currency.is_base_currency,
      is_active: currency.is_active,
    });
    setOpenForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this currency?')) {
      try {
        await axios.delete(`${API_BASE_URL}/currencies/${id}`);
        fetchCurrencies();
      } catch (err) {
        setError(err.response?.data?.detail || err.message);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedCurrency) {
        await axios.put(
          `${API_BASE_URL}/currencies/${selectedCurrency.id}`,
          {
            name: formData.name,
            symbol: formData.symbol,
            is_base_currency: formData.is_base_currency,
            is_active: formData.is_active,
          }
        );
      } else {
        await axios.post(`${API_BASE_URL}/currencies/`, formData);
      }
      fetchCurrencies();
      setOpenForm(false);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  const handleFetchRates = async () => {
    if (!window.confirm('Fetch latest exchange rates from external API?')) return;
    
    try {
      setLoading(true);
      const baseCurrency = currencies.find(c => c.is_base_currency);
      const response = await axios.post(
        `${API_BASE_URL}/currencies/exchange-rates/fetch-from-api`,
        null,
        { params: { base_currency_code: baseCurrency?.code || 'USD' } }
      );
      alert(response.data.message);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Currency Management</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleFetchRates}
            sx={{ mr: 2 }}
            disabled={loading}
          >
            Fetch Rates
          </Button>
          <Button
            variant="contained"
            color="primary"
            startIcon={<Add />}
            onClick={handleAdd}
          >
            Add Currency
          </Button>
        </Box>
      </Box>

      {error && (
        <Box mb={2}>
          <Typography color="error">{error}</Typography>
        </Box>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Symbol</TableCell>
              <TableCell>Base Currency</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {currencies.map((currency) => (
              <TableRow key={currency.id}>
                <TableCell>
                  <strong>{currency.code}</strong>
                </TableCell>
                <TableCell>{currency.name}</TableCell>
                <TableCell>{currency.symbol}</TableCell>
                <TableCell>
                  {currency.is_base_currency && (
                    <Chip
                      icon={<Star />}
                      label="Base"
                      color="warning"
                      size="small"
                    />
                  )}
                </TableCell>
                <TableCell>
                  <Chip
                    label={currency.is_active ? 'Active' : 'Inactive'}
                    color={currency.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton onClick={() => handleEdit(currency)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton
                    onClick={() => handleDelete(currency.id)}
                    color="error"
                    disabled={currency.is_base_currency}
                  >
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openForm} onClose={() => setOpenForm(false)} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedCurrency ? 'Edit Currency' : 'Add Currency'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  name="code"
                  label="Currency Code (ISO 4217)"
                  value={formData.code}
                  onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                  fullWidth
                  required
                  inputProps={{ maxLength: 3 }}
                  disabled={!!selectedCurrency}
                  helperText="e.g., USD, EUR, GBP"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="name"
                  label="Currency Name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="symbol"
                  label="Symbol"
                  value={formData.symbol}
                  onChange={(e) => setFormData({ ...formData, symbol: e.target.value })}
                  fullWidth
                  helperText="e.g., $, €, £"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={formData.is_base_currency}
                      onChange={(e) =>
                        setFormData({ ...formData, is_base_currency: e.target.checked })
                      }
                    />
                  }
                  label="Set as Base Currency (Library Currency)"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={formData.is_active}
                      onChange={(e) =>
                        setFormData({ ...formData, is_active: e.target.checked })
                      }
                    />
                  }
                  label="Active"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenForm(false)}>Cancel</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedCurrency ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default CurrencyManagement;
