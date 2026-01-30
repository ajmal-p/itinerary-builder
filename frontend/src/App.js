import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppProvider } from './store/AppContext';

// Common components
import Navbar from './components/common/Navbar';

// Pages
import Home from './pages/Home';
import HotelList from './components/hotels/HotelList';
import ActivityList from './components/activities/ActivityList';
import TransferList from './components/transfers/TransferList';
import MealList from './components/meals/MealList';
import CustomerList from './components/customers/CustomerList';
import EnquiryList from './components/enquiries/EnquiryList';
import ItineraryList from './components/itineraries/ItineraryList';
import ItineraryBuilder from './components/itineraries/ItineraryBuilder';
import QuoteList from './components/quotes/QuoteList';
import CurrencyManagement from './components/currencies/CurrencyManagement';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/hotels" element={<HotelList />} />
            <Route path="/activities" element={<ActivityList />} />
            <Route path="/transfers" element={<TransferList />} />
            <Route path="/meals" element={<MealList />} />
            <Route path="/customers" element={<CustomerList />} />
            <Route path="/enquiries" element={<EnquiryList />} />
            <Route path="/itineraries" element={<ItineraryList />} />
            <Route path="/itineraries/:id" element={<ItineraryBuilder />} />
            <Route path="/quotes" element={<QuoteList />} />
            <Route path="/currencies" element={<CurrencyManagement />} />
          </Routes>
        </Router>
      </AppProvider>
    </ThemeProvider>
  );
}

export default App;
