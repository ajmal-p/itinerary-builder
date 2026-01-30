import React from 'react';
import { Alert, Box } from '@mui/material';

const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <Box mb={2}>
      <Alert severity="error">{message}</Alert>
    </Box>
  );
};

export default ErrorMessage;
