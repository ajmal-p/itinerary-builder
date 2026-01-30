import api from './api';

export const hotelService = {
  getAll: (skip = 0, limit = 100) => api.get(`/hotels?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/hotels/${id}`),
  create: (data) => api.post('/hotels', data),
  update: (id, data) => api.put(`/hotels/${id}`, data),
  delete: (id) => api.delete(`/hotels/${id}`),
};

export const activityService = {
  getAll: (skip = 0, limit = 100) => api.get(`/activities?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/activities/${id}`),
  create: (data) => api.post('/activities', data),
  update: (id, data) => api.put(`/activities/${id}`, data),
  delete: (id) => api.delete(`/activities/${id}`),
};

export const transferService = {
  getAll: (skip = 0, limit = 100) => api.get(`/transfers?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/transfers/${id}`),
  create: (data) => api.post('/transfers', data),
  update: (id, data) => api.put(`/transfers/${id}`, data),
  delete: (id) => api.delete(`/transfers/${id}`),
};

export const mealService = {
  getAll: (skip = 0, limit = 100) => api.get(`/meals?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/meals/${id}`),
  create: (data) => api.post('/meals', data),
  update: (id, data) => api.put(`/meals/${id}`, data),
  delete: (id) => api.delete(`/meals/${id}`),
};

export const customerService = {
  getAll: (skip = 0, limit = 100) => api.get(`/customers?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/customers/${id}`),
  create: (data) => api.post('/customers', data),
  update: (id, data) => api.put(`/customers/${id}`, data),
  delete: (id) => api.delete(`/customers/${id}`),
};

export const enquiryService = {
  getAll: (skip = 0, limit = 100) => api.get(`/enquiries?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/enquiries/${id}`),
  getByCustomer: (customerId) => api.get(`/enquiries/customer/${customerId}`),
  create: (data) => api.post('/enquiries', data),
  update: (id, data) => api.put(`/enquiries/${id}`, data),
  delete: (id) => api.delete(`/enquiries/${id}`),
};

export const itineraryService = {
  getAll: (skip = 0, limit = 100) => api.get(`/itineraries?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/itineraries/${id}`),
  create: (data) => api.post('/itineraries', data),
  update: (id, data) => api.put(`/itineraries/${id}`, data),
  delete: (id) => api.delete(`/itineraries/${id}`),
  addItem: (itineraryId, data) => api.post(`/itineraries/${itineraryId}/items`, data),
  getItems: (itineraryId) => api.get(`/itineraries/${itineraryId}/items`),
  updateItem: (itemId, data) => api.put(`/itineraries/items/${itemId}`, data),
  deleteItem: (itemId) => api.delete(`/itineraries/items/${itemId}`),
};

export const quoteService = {
  getAll: (skip = 0, limit = 100) => api.get(`/quotes?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/quotes/${id}`),
  getByEnquiry: (enquiryId) => api.get(`/quotes/enquiry/${enquiryId}`),
  create: (data) => api.post('/quotes', data),
  update: (id, data) => api.put(`/quotes/${id}`, data),
  delete: (id) => api.delete(`/quotes/${id}`),
  exportPDF: (id) => api.get(`/quotes/${id}/pdf`, { responseType: 'blob' }),
};
