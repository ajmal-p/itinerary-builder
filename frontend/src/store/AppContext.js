import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  hotelService,
  activityService,
  transferService,
  mealService,
  customerService,
  enquiryService,
  itineraryService,
  quoteService,
} from '../services';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [hotels, setHotels] = useState([]);
  const [activities, setActivities] = useState([]);
  const [transfers, setTransfers] = useState([]);
  const [meals, setMeals] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [enquiries, setEnquiries] = useState([]);
  const [itineraries, setItineraries] = useState([]);
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHotels = async () => {
    try {
      setLoading(true);
      const response = await hotelService.getAll();
      setHotels(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchActivities = async () => {
    try {
      setLoading(true);
      const response = await activityService.getAll();
      setActivities(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchTransfers = async () => {
    try {
      setLoading(true);
      const response = await transferService.getAll();
      setTransfers(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchMeals = async () => {
    try {
      setLoading(true);
      const response = await mealService.getAll();
      setMeals(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await customerService.getAll();
      setCustomers(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchEnquiries = async () => {
    try {
      setLoading(true);
      const response = await enquiryService.getAll();
      setEnquiries(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchItineraries = async () => {
    try {
      setLoading(true);
      const response = await itineraryService.getAll();
      setItineraries(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchQuotes = async () => {
    try {
      setLoading(true);
      const response = await quoteService.getAll();
      setQuotes(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const value = {
    hotels,
    activities,
    transfers,
    meals,
    customers,
    enquiries,
    itineraries,
    quotes,
    loading,
    error,
    fetchHotels,
    fetchActivities,
    fetchTransfers,
    fetchMeals,
    fetchCustomers,
    fetchEnquiries,
    fetchItineraries,
    fetchQuotes,
    setHotels,
    setActivities,
    setTransfers,
    setMeals,
    setCustomers,
    setEnquiries,
    setItineraries,
    setQuotes,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
