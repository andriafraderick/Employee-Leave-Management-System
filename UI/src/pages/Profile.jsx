import { useEffect, useState, useRef } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  TextField,
  Button,
  Divider,
  Grid,
  Link,
  Chip
} from '@mui/material';
import { Logout, ArrowBack, CameraAlt, GitHub, Launch } from '@mui/icons-material';
import { styled } from '@mui/system';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// Styled components
const FullHeightBox = styled(Box)({
  minHeight: '100vh',
  backgroundImage: 'linear-gradient(rgba(103, 58, 183, 0.9), rgba(63, 81, 181, 0.9)), url(/bg.jpeg)',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundAttachment: 'fixed',
  padding: '20px',
  paddingTop: '60px' // Adjusted for taller AppBar
});

const ProfileContainer = styled(Box)({
  width: '100%',
  maxWidth: '1200px',
  overflowX: 'hidden', 
  margin: '0 auto',
  padding: '40px',
  borderRadius: '16px',
  backgroundColor: 'rgba(103, 58, 183, 0.2)',
  backdropFilter: 'blur(10px)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)'
});

const ProfileImageContainer = styled(Box)({
  position: 'relative',
  display: 'inline-block',
  width: 140,
  height: 140,
  marginBottom: 24,
});

const CameraIconLabel = styled('label')({
  position: 'absolute',
  bottom: 0,
  right: 0,
  backgroundColor: 'rgba(103, 58, 183, 0.9)',
  borderRadius: '50%',
  padding: 8,
  boxShadow: '0 0 12px rgba(0,0,0,0.3)',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: 'rgba(103, 58, 183, 1)',
    transform: 'scale(1.1)'
  }
});

const HiddenInput = styled('input')({
  display: 'none',
});

const TechChip = styled(Chip)({
  margin: '4px',
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  color: '#fff',
  border: '1px solid rgba(255, 255, 255, 0.3)'
});

// Helper to convert file to base64
function convertToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

const Profile = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [profileData, setProfileData] = useState({});
  const [image, setImage] = useState(null);

  useEffect(() => {
    if (!user?.employee_id) return;
    fetchProfileData();
  }, [user]);

  const fetchProfileData = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/profile/${user.employee_id}`);
      setProfileData(res.data);
      setImage(res.data.profile_image || null);
    } catch (err) {
      console.error('Failed to fetch profile data:', err);
    }
  };

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      try {
        const base64 = await convertToBase64(file);
        setImage(base64);
        setProfileData((prev) => ({ ...prev, profile_image: base64 }));
      } catch (err) {
        console.error('Error converting to base64:', err);
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async () => {
    try {
      await axios.post(`http://localhost:8000/profile/update`, profileData);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error('Error saving profile:', err);
    }
  };

  const renderLinkField = (value) => {
    if (!value) return '';
    if (value.includes(',')) {
      return value.split(',').map((link, i) => (
        <Box key={i} mb={1}>
          <Link 
            href={link.trim()} 
            target="_blank" 
            rel="noopener"
            sx={{
              color: '#bb86fc',
              display: 'flex',
              alignItems: 'center',
              textDecoration: 'none',
              '&:hover': {
                textDecoration: 'underline'
              }
            }}
          >
            <GitHub fontSize="small" sx={{ mr: 1 }} />
            {link.trim()}
            <Launch fontSize="small" sx={{ ml: 1 }} />
          </Link>
        </Box>
      ));
    }
    return (
      <Link 
        href={value} 
        target="_blank" 
        rel="noopener"
        sx={{
          color: '#bb86fc',
          display: 'flex',
          alignItems: 'center',
          textDecoration: 'none',
          '&:hover': {
            textDecoration: 'underline'
          }
        }}
      >
        <GitHub fontSize="small" sx={{ mr: 1 }} />
        {value}
        <Launch fontSize="small" sx={{ ml: 1 }} />
      </Link>
    );
  };

  const renderTechStack = (value) => {
    if (!value) return '';
    const items = value.includes(',') ? value.split(',') : [value];
    return (
      <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
        {items.map((tech, i) => (
          <TechChip key={i} label={tech.trim()} />
        ))}
      </Box>
    );
  };

  const editableFields = [
    'gender',
    'address',
    'blood_type',
    'headquarters_address',
    'office_locations',
    'phone_number',
    'social_links',
    'specializations',
    'products_services',
    'certifications_awards',
    'tech_stack',
    'events_hosted',
    'clients_partners',
    'executives',
    'open_source_links'
  ];

  const readOnlyFields = [
    { label: 'Employee ID', name: 'employee_id' },
    { label: 'Name', name: 'name' },
    { label: 'Designation', name: 'designation' },
    { label: 'Role', name: 'role' },
    { label: 'Status', name: 'status' },
    { label: 'Email', name: 'email' },
    { label: 'Manager ID', name: 'manager_id' },
  ];

  const customRenderFields = {
    'tech_stack': renderTechStack,
    'open_source_links': renderLinkField,
    'social_links': renderLinkField
  };

  if (!user || !profileData) return <div>Loading...</div>;

  return (
    <FullHeightBox>
      <AppBar position="fixed" sx={{ 
        height: '60px', 
        overflowX: 'hidden',
        backgroundColor: '#673ab7',
        backdropFilter: 'blur(10px)',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
      }}>
        <Toolbar sx={{ minHeight: '60px !important' }}>
          <IconButton edge="start" color="inherit" onClick={() => navigate('/dashboard')}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" sx={{ 
            flexGrow: 1, 
            textAlign: 'center', 
            fontWeight: 600,
            letterSpacing: '1px'
          }}>
            EMPLOYEE PROFILE
          </Typography>
          <IconButton edge="end" color="inherit" onClick={logout}>
            <Logout />
          </IconButton>
        </Toolbar>
      </AppBar>

      <ProfileContainer>
        <Typography variant="h4" gutterBottom sx={{ 
          fontWeight: 700,
          color: '#fff',
          mb: 4,
          letterSpacing: '0.5px'
        }}>
          Welcome, <span style={{ color: '#bb86fc' }}>{profileData.name || 'User'}</span>
        </Typography>

        <Divider sx={{ 
          my: 4, 
          borderColor: 'rgba(255, 255, 255, 0.2)',
          borderWidth: '1px'
        }} />

        <Box display="flex" justifyContent="center">
          <ProfileImageContainer>
            <Avatar
              src={image}
              sx={{ 
                width: 140, 
                height: 140, 
                fontSize: 48, 
                bgcolor: '#bb86fc',
                boxShadow: '0 4px 20px rgba(187, 134, 252, 0.3)'
              }}
            >
              {!image && profileData.name?.[0]?.toUpperCase()}
            </Avatar>
            <CameraIconLabel htmlFor="upload-input">
              <CameraAlt fontSize="small" />
            </CameraIconLabel>
            <HiddenInput
              id="upload-input"
              type="file"
              accept="image/*"
              ref={fileInputRef}
              onChange={handleUpload}
            />
          </ProfileImageContainer>
        </Box>

        <Grid container spacing={4} sx={{ mt: 2 }}>
          {readOnlyFields.map(({ label, name }) => (
            <Grid item xs={12} sm={6} md={4} key={name}>
              <TextField
                fullWidth
                label={label}
                name={name}
                value={profileData[name] || ''}
                InputProps={{ 
                  readOnly: true,
                  sx: {
                    color: '#fff',
                    '& input': {
                      color: '#fff'
                    }
                  }
                }}
                InputLabelProps={{
                  sx: {
                    color: 'rgba(255, 255, 255, 0.7)',
                  }
                }}
                variant="outlined"
                size="small"
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.3)',
                    },
                    '&:hover fieldset': {
                      borderColor: '#bb86fc',
                    },
                  },
                }}
              />
            </Grid>
          ))}

          {editableFields.map((field) => (
            <Grid item xs={12} sm={6} md={4} key={field}>
              {customRenderFields[field] ? (
                <Box>
                  <Typography variant="caption" sx={{
                    display: 'block',
                    color: 'rgba(255, 255, 255, 0.7)',
                    mb: 1,
                    fontSize: '0.75rem'
                  }}>
                    {field.replace(/_/g, ' ').toUpperCase()}
                  </Typography>
                  <Box sx={{
                    minHeight: '40px',
                    padding: '8px 14px',
                    borderRadius: '4px',
                    border: '1px solid rgba(255, 255, 255, 0.3)',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)'
                  }}>
                    {customRenderFields[field](profileData[field] || '')}
                  </Box>
                </Box>
              ) : (
                <TextField
                  fullWidth
                  label={field.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                  name={field}
                  value={profileData[field] || ''}
                  onChange={handleChange}
                  InputProps={{
                    sx: {
                      color: '#fff',
                      '& input': {
                        color: '#fff'
                      }
                    }
                  }}
                  InputLabelProps={{
                    sx: {
                      color: 'rgba(255, 255, 255, 0.7)',
                    }
                  }}
                  variant="outlined"
                  size="small"
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.3)',
                      },
                      '&:hover fieldset': {
                        borderColor: '#bb86fc',
                      },
                    },
                  }}
                />
              )}
            </Grid>
          ))}
        </Grid>

        <Box mt={6} display="flex" justifyContent="flex-end">
          <Button 
            variant="contained" 
            size="large" 
            onClick={handleSave}
            sx={{
              backgroundColor: '#bb86fc',
              color: '#000',
              fontWeight: 700,
              px: 5,
              py: 1.5,
              borderRadius: '8px',
              letterSpacing: '1px',
              '&:hover': {
                backgroundColor: '#a370d8',
                boxShadow: '0 4px 15px rgba(187, 134, 252, 0.4)'
              }
            }}
          >
            SAVE CHANGES
          </Button>
        </Box>
      </ProfileContainer>
    </FullHeightBox>
  );
};

export default Profile;