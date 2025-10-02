import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  CircularProgress, Box, Button, Typography, TextField, MenuItem, Select, FormControl, InputLabel,
  Avatar, IconButton, Tooltip, InputAdornment, Snackbar, Alert, Pagination
} from '@mui/material';

import {
  Home as HomeIcon,
  AccountCircle as ProfileIcon,
  Logout as LogoutIcon,
  Search as SearchIcon
} from '@mui/icons-material';

import ExcelJS from 'exceljs';
import { saveAs } from 'file-saver';

const Dashboard = () => {
  const { user, token, logout } = useAuth();
  const [leaveData, setLeaveData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lopValues, setLopValues] = useState({});
  const [selectedYear, setSelectedYear] = useState(2025);
  const [selectedMonth, setSelectedMonth] = useState(7);
  const [searchText, setSearchText] = useState('');
  const [page, setPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [totalCount, setTotalCount] = useState(0);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  const navigate = useNavigate();

  const monthOptions = [...Array(12)].map((_, i) => ({
    label: new Date(0, i).toLocaleString('default', { month: 'long' }),
    value: i + 1
  }));

  const yearOptions = [2025, 2024, 2023, 2022, 2021, 2020];

  useEffect(() => {
    const savedLOP = localStorage.getItem('lopValues');
    if (savedLOP) {
      try {
        setLopValues(JSON.parse(savedLOP));
      } catch (e) {
        console.error("Failed to parse LOP from localStorage");
      }
    }
  }, []);

  useEffect(() => {
  setPage(1);
}, [selectedMonth, selectedYear, searchText]);


useEffect(() => {
  const fetchLeaveData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        'http://127.0.0.1:8000/combined/all_leave_details',
        {
          params: {
            year: selectedYear,
            month: selectedMonth,
            search: searchText,
            limit: rowsPerPage,
            offset: (page - 1) * rowsPerPage,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = response.data?.data || [];
      setLeaveData(data);
      setTotalCount(response.data?.total || 0);

      setLopValues(prev => {
        const updated = { ...prev };
        data.forEach(emp => {
          if (!(emp.employee_id in updated)) {
            updated[emp.employee_id] = '';
          }
        });
        return updated;
      });

      setLoading(false);
    } catch (err) {
      console.error(err);
      setError("Failed to load leave data");
      setLoading(false);
    }
  };

  if (token) {
    fetchLeaveData();
  }
}, [
  token,
  selectedMonth,
  selectedYear,
  searchText,
  page,
  rowsPerPage,  
]);

useEffect(() => {
  setPage(1);
}, [selectedMonth, selectedYear, searchText, rowsPerPage]);



  const handleLOPChange = (empId, value) => {
    const numericValue = value.replace(/[^0-9]/g, '');
    setLopValues(prev => {
      const updated = { ...prev, [empId]: numericValue };
      localStorage.setItem('lopValues', JSON.stringify(updated));
      return updated;
    });
  };

  const handleApply = async (empId) => {
    const lopValue = Number(lopValues[empId]) || 0;
    if (lopValue <= 0) return;

    try {
      const employee = leaveData.find(emp => emp.employee_id === empId);
      
      if (!employee) {
        throw new Error("Employee not found");
      }

      const payload = {
        employee_id: empId,
        remaining_leaves: (employee.remaining_leaves || 0) + lopValue,
        total_leaves: employee.total_leaves || 15,
        year: selectedYear,
        leave_type: 'casual'
      };

      if (employee.leave_detail_id) {
        payload.leave_detail_id = employee.leave_detail_id;
      }

      const response = await axios.post(
        'http://127.0.0.1:8000/remaining-leaves/',
        payload
      );

      setLeaveData(prev => prev.map(emp => 
        emp.employee_id === empId ? 
        { 
          ...emp, 
          remaining_leaves: payload.remaining_leaves,
          leave_detail_id: response.data.id
        } : 
        emp
      ));

      setLopValues(prev => ({ ...prev, [empId]: '' }));

      setSnackbar({
        open: true,
        message: `Leave balance updated successfully!`,
        severity: 'success'
      });

    } catch (err) {
      console.error("Application error:", {
        error: err.response?.data || err.message,
        employeeData: leaveData.find(e => e.employee_id === empId)
      });

      setSnackbar({
        open: true,
        message: err.response?.data?.detail || 
                `Failed to update leave: ${err.message}`,
        severity: 'error'
      });
    }
  };

  const handleDownload = async () => {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Leave Summary');
    worksheet.columns = [
      { header: 'Employee ID', key: 'employee_id', width: 15 },
      { header: 'Employee Name', key: 'employee_name', width: 25 },
      { header: 'Total Leaves', key: 'total_leaves', width: 15 },
      { header: 'Remaining Leaves', key: 'remaining_leaves', width: 18 },
      { header: 'LOP', key: 'lop', width: 10 },
    ];
    leaveData.forEach(emp => {
      worksheet.addRow({
        employee_id: emp.employee_id,
        employee_name: emp.employee_name,
        total_leaves: emp.total_leaves,
        remaining_leaves: emp.remaining_leaves,
        lop: lopValues[emp.employee_id] || '',
      });
    });
    const buffer = await workbook.xlsx.writeBuffer();
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    saveAs(blob, `leave_summary_${selectedMonth}_${selectedYear}.xlsx`);
  };

  const getInitials = (name) => {
    if (!name) return '';
    const [first, second] = name.split(' ');
    return `${first?.[0] || ''}${second?.[0] || ''}`.toUpperCase();
  };

  const selectedMonthLabel = monthOptions.find(m => m.value === selectedMonth)?.label;

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundImage: 'linear-gradient(rgba(103, 58, 183, 0.8), rgba(63, 81, 181, 0.8)), url(/bg.jpeg)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed',
      pb: 4
    }}>
      {/* AppBar - Height is approximately 1.5cm (56px) */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          bgcolor: 'rgba(25, 118, 210, 0.9)',
          color: '#fff',
          px: 3,
          py: 2,
          boxShadow: 3,
          backdropFilter: 'blur(10px)',
          position: 'sticky',
          top: 0,
          zIndex: 1100
        }}
      >
        <IconButton onClick={() => navigate('/dashboard')} color="inherit">
          <HomeIcon />
        </IconButton>

        <Typography variant="h6" fontWeight={600}>Dashboard</Typography>

        <Box display="flex" alignItems="center" gap={1}>
          <Tooltip title="Profile">
            <IconButton onClick={() => navigate('/profile')} color="inherit">
              {user?.profileImage ? (
                <Avatar alt={user.name} src={user.profileImage} />
              ) : (
                <Avatar sx={{ bgcolor: '#f50057' }}>
                  {getInitials(user?.name)}
                </Avatar>
              )}
            </IconButton>
          </Tooltip>
          <Tooltip title="Logout">
            <IconButton onClick={logout} color="inherit">
              <LogoutIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Main Content */}
      <Box sx={{ p: 4 }}>
        <Paper elevation={0} sx={{ 
          p: 3, 
          borderRadius: 3,
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h5" fontWeight={600} color="text.primary">
              Welcome, {user?.name}
            </Typography>
          </Box>

          <Typography variant="subtitle1" gutterBottom color="text.secondary">
            Role: {user?.role}
          </Typography>

          <Box display="flex" flexWrap="wrap" gap={2} alignItems="center" justifyContent="space-between" mb={3}>
            <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Month</InputLabel>
                <Select
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(e.target.value)}
                  label="Month"
                >
                  {monthOptions.map((m) => (
                    <MenuItem key={m.value} value={m.value}>{m.label}</MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Year</InputLabel>
                <Select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(e.target.value)}
                  label="Year"
                >
                  {yearOptions.map((y) => (
                    <MenuItem key={y} value={y}>{y}</MenuItem>
                  ))}
                </Select>
              </FormControl>

              <TextField
                size="small"
                placeholder="Search by ID or name"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                sx={{ minWidth: 240 }}
              />
            </Box>

            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleDownload}
              sx={{
                fontWeight: 600,
                textTransform: 'none',
                boxShadow: 'none',
                '&:hover': {
                  boxShadow: '0 2px 5px rgba(0, 0, 0, 0.2)'
                }
              }}
            >
              Download .xlsx ({selectedMonthLabel} {selectedYear})
            </Button>
          </Box>

          <Typography variant="h6" gutterBottom color="text.primary">
            Leave Summary ({selectedMonthLabel} {selectedYear})
          </Typography>

          {loading ? (
            <Box display="flex" justifyContent="center" mt={3}>
              <CircularProgress />
            </Box>
          ) : (
            <TableContainer component={Paper} sx={{ 
              mt: 2, 
              borderRadius: 2,
              boxShadow: 'none',
              border: '1px solid rgba(0, 0, 0, 0.1)',
              backgroundColor: 'rgba(255, 255, 255, 0.7)'
            }}>
              <Table size="small" sx={{
                '& .MuiTableCell-root': {
                  borderRight: '1px solid rgba(0, 0, 0, 0.08)',
                  '&:last-child': {
                    borderRight: 'none'
                  }
                }
              }}>
                <TableHead>
                  <TableRow sx={{ 
                    backgroundColor: 'rgba(25, 118, 210, 0.1)',
                    '& th': {
                      fontWeight: 'bold',
                      color: 'text.primary'
                    }
                  }}>
                    <TableCell>Employee ID</TableCell>
                    <TableCell>Employee Name</TableCell>
                    <TableCell>Total Leaves</TableCell>
                    <TableCell>Remaining Leaves</TableCell>
                    <TableCell>LOP</TableCell>
                    <TableCell>Action</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {leaveData.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        No leave summary found.
                      </TableCell>
                    </TableRow>
                  ) : (
                    leaveData.map((emp) => (
                      <TableRow key={emp.employee_id} hover sx={{ 
                        '&:last-child td': { borderBottom: 0 },
                        '&:hover': {
                          backgroundColor: 'rgba(25, 118, 210, 0.03)'
                        }
                      }}>
                        <TableCell>{emp.employee_id}</TableCell>
                        <TableCell>{emp.employee_name}</TableCell>
                        <TableCell>
                        <Tooltip 
                           title={emp.leave_types || "No leaves taken"} 
                           arrow 
                           placement="top"
                        >
                           <Tooltip title={emp.leave_types || "No leaves taken"} arrow placement="top">
  <span>{emp.total_leaves}</span>
</Tooltip>

                           </Tooltip>
                        </TableCell>

                        <TableCell>{emp.remaining_leaves}</TableCell>
                        <TableCell>
                          <TextField
                            variant="outlined"
                            size="small"
                            value={lopValues[emp.employee_id] || ''}
                            onChange={(e) => handleLOPChange(emp.employee_id, e.target.value)}
                            inputProps={{
                              inputMode: 'numeric',
                              pattern: '[0-9]*',
                            }}
                            sx={{
                              maxWidth: 60,
                              input: { 
                                textAlign: 'center', 
                                fontSize: '0.85rem', 
                                py: 0.5,
                                '&::-webkit-outer-spin-button, &::-webkit-inner-spin-button': {
                                  '-webkit-appearance': 'none',
                                  margin: 0,
                                },
                                '&[type=number]': {
                                  '-moz-appearance': 'textfield',
                                },
                              },
                            }}
                          />
                        </TableCell>
                        <TableCell>
                          <Button 
                            variant="contained" 
                            color="primary" 
                            size="small"
                            onClick={() => handleApply(emp.employee_id)}
                            disabled={!lopValues[emp.employee_id] || isNaN(lopValues[emp.employee_id]) || Number(lopValues[emp.employee_id]) <= 0}
                            sx={{
                              textTransform: 'none',
                              fontWeight: 500,
                              boxShadow: 'none'
                            }}
                          >
                            Apply
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          <Box display="flex" justifyContent="flex-end" alignItems="center" mt={2}>
  <Typography variant="body2" sx={{ mr: 1 }}>Rows per page:</Typography>
  <Select
    size="small"
    value={rowsPerPage}
    onChange={(e) => {
      setRowsPerPage(parseInt(e.target.value));
      setPage(1); // reset to page 1 when rows per page changes
    }}
  >
    {[5, 10, 15, 20, 50].map((num) => (
      <MenuItem key={num} value={num}>{num}</MenuItem>
    ))}
  </Select>
</Box>
          {totalCount > rowsPerPage && (
            <Box display="flex" justifyContent="center" mt={3}>
              <Pagination
                count={Math.ceil(totalCount / rowsPerPage)}
                page={page}
                onChange={(e, newPage) => setPage(newPage)}
                color="primary"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </Paper>
      </Box>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Dashboard;