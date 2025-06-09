interface AuthResponse {
  data: any;
  success: boolean;
  message: string;
  token?: string;
}

interface SignUpData {
  username: string;
  email: string;
  password: string;
}

interface SignInData {
  email: string;
  password: string;
}

class AuthService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  async signUp(data: SignUpData): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      return await response.json();
    } catch (error) {
      console.error('Sign up error:', error);
      return {
        success: false,
        message: 'An error occurred during sign up',
      };
    }
  }

  async signIn(data: SignInData): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      return await response.json();
    } catch (error) {
      console.error('Sign in error:', error);
      return {
        success: false,
        message: 'An error occurred during sign in',
      };
    }
  }

  saveToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  removeToken() {
    localStorage.removeItem('token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export const authService = new AuthService();
