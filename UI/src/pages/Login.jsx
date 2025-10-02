import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Box,
  Typography,
  TextField,
  Button,
  Divider,
  Link,
  InputAdornment,
  IconButton
} from '@mui/material';
import {
  LockOutlined,
  Visibility,
  VisibilityOff,
  EmailOutlined
} from '@mui/icons-material';

export default function Login() {
  const { login, error } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [localError, setLocalError] = useState('');
  const navigate = useNavigate();

  // Ensure body doesn't scroll on this page
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = '';
      document.documentElement.style.overflow = '';
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(email, password);
    if (result.success) {
      navigate('/dashboard');
    } else {
      setLocalError(result.error || 'Invalid email or password');
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        overflow: 'hidden',
        backgroundImage: 'url(/bg.jpeg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <Box
        sx={{
          width: '100%',
          maxWidth: 400,
          p: 4,
        }}
      >
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            mb: 4
          }}
        >
          <LockOutlined
            sx={{
              fontSize: 40,
              color: 'white',
              bgcolor: 'rgba(255, 255, 255, 0.1)',
              p: 2,
              borderRadius: '50%'
            }}
          />
        </Box>

        <Typography
          variant="h5"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 600,
            color: 'white',
            textAlign: 'center',
            mb: 1
          }}
        >
          Welcome back
        </Typography>

        <Typography
          variant="body2"
          sx={{
            mb: 4,
            color: 'rgba(255, 255, 255, 0.7)',
            textAlign: 'center'
          }}
        >
          Enter your credentials to access your account
        </Typography>

        {(localError || error) && (
          <Typography
            sx={{
              mb: 2,
              textAlign: 'center',
              fontSize: '0.875rem',
              backgroundColor: 'rgba(239, 68, 68, 0.2)',
              color: 'white',
              p: 1,
              borderRadius: '4px'
            }}
          >
            {localError || error}
          </Typography>
        )}

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <Typography
            variant="body1"
            component="label"
            htmlFor="email"
            sx={{
              display: 'block',
              fontSize: '0.95rem',
              fontWeight: 'bold',
              color: 'rgba(255, 255, 255, 0.9)',
              textTransform: 'uppercase',
              mb: 1,
              ml: 1
            }}
          >
            EMAIL ADDRESS
          </Typography>

          <TextField
            margin="none"
            required
            fullWidth
            id="email"
            name="email"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start" sx={{ mr: 2 }}>
                  <EmailOutlined
                    sx={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: 20
                    }}
                  />
                </InputAdornment>
              ),
            }}
            sx={{
              mb: 3,
              '& .MuiOutlinedInput-root': {
                borderRadius: '8px',
                color: 'white',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.2)',
                },
                '&:hover fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.3)',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.5)',
                  boxShadow: '0 0 0 2px rgba(255, 255, 255, 0.1)'
                },
              }
            }}
          />

          <Typography
            variant="body1"
            component="label"
            htmlFor="password"
            sx={{
              display: 'block',
              fontSize: '0.95rem',
              fontWeight: 'bold',
              color: 'rgba(255, 255, 255, 0.9)',
              textTransform: 'uppercase',
              mb: 1,
              ml: 1
            }}
          >
            PASSWORD
          </Typography>

          <TextField
            margin="none"
            required
            fullWidth
            name="password"
            type={showPassword ? 'text' : 'password'}
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start" sx={{ mr: 2 }}>
                  <LockOutlined
                    sx={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: 20
                    }}
                  />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => setShowPassword(!showPassword)}
                    edge="end"
                    sx={{ color: 'rgba(255, 255, 255, 0.7)' }}
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
            sx={{
              mb: 3,
              '& .MuiOutlinedInput-root': {
                borderRadius: '8px',
                color: 'white',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.2)',
                },
                '&:hover fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.3)',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.5)',
                  boxShadow: '0 0 0 2px rgba(255, 255, 255, 0.1)'
                },
              }
            }}
          />

          <Box sx={{ textAlign: 'right', mb: 1.5 }}>
            <Link
              href="#"
              variant="body2"
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                fontSize: '0.775rem',
                fontWeight: 500,
                textDecoration: 'none',
                '&:hover': {
                  color: 'white',
                  textDecoration: 'underline'
                }
              }}
            >
              Forgot password?
            </Link>
          </Box>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{
              mt: 1,
              mb: 1.5,
              py: 1.5,
              borderRadius: '8px',
              fontSize: '0.8375rem',
              fontWeight: 600,
              textTransform: 'none',
              backgroundColor: 'white',
              color: '#673ab7',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
              }
            }}
          >
            Sign In
          </Button>

          <Divider sx={{ my: 1.5, borderColor: 'rgba(255, 255, 255, 0.2)' }}>
            <Typography variant="body2" sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              px: 2,
              fontSize: '0.775rem'
            }}>
              OR
            </Typography>
          </Divider>

          <Box sx={{ textAlign: 'center', mt: 1.5 }}>
            <Typography variant="body2" sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              fontSize: '0.775rem'
            }}>
              Don't have an account?{' '}
              <Link
                href="#"
                sx={{
                  color: 'white',
                  fontWeight: 600,
                  textDecoration: 'none',
                  fontSize: '0.775rem',
                  '&:hover': {
                    textDecoration: 'underline'
                  }
                }}
              >
                Contact admin
              </Link>
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
}
