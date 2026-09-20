import React, { useState, useEffect } from 'react';
import { 
  User, 
  Mail, 
  Target, 
  FileText, 
  Flame, 
  Clock, 
  Award, 
  CheckCircle, 
  RefreshCw,
  LogOut
} from 'lucide-react';
import { api } from '../api';
import { useNavigate } from 'react-router-dom';
import { ROLE_CATEGORIES } from '../rolesConfig';

export default function Profile({ onLogout }) {
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [targetRole, setTargetRole] = useState('');
  const [updating, setUpdating] = useState(false);
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await api.me();
        setProfile(data.user);
        setTargetRole(data.user.target_role || 'ML Engineer');
      } catch (err) {
        console.error('Failed to load profile:', err);
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  const handleUpdateRole = async () => {
    setUpdating(true);
    setSuccess('');
    try {
      await api.updateTargetRole(targetRole);
      setSuccess('Target role updated! Curriculum recommendations refreshed.');
    } catch (err) {
      console.error(err);
    } finally {
      setUpdating(false);
    }
  };

  const handleLogout = async () => {
    await api.logout();
    if (onLogout) onLogout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <RefreshCw size={36} color="#818cf8" style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '2rem', marginBottom: '4px' }}>Learner Profile</h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Manage your account credentials, target career goal, and learning preferences.
        </p>
      </div>

      {success && (
        <div style={{
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          padding: '1rem',
          borderRadius: '12px',
          color: '#6ee7b7',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <CheckCircle size={20} />
          <span>{success}</span>
        </div>
      )}

      {/* Profile Overview Card */}
      <div className="glass-card" style={{ padding: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '2rem' }}>
          <div style={{
            width: '72px',
            height: '72px',
            borderRadius: '20px',
            background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 8px 24px rgba(99, 102, 241, 0.4)'
          }}>
            <User size={36} color="#fff" />
          </div>

          <div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '4px' }}>{profile?.username}</h2>
            <div style={{ display: 'flex', gap: '14px', fontSize: '0.88rem', color: 'var(--text-muted)' }}>
              <span>✉ {profile?.email || 'learner@skillpath.ai'}</span>
            </div>
          </div>
        </div>

        {/* Learning Stats Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#f59e0b', marginBottom: '6px' }}>
              <Flame size={18} />
              <span style={{ fontSize: '0.8rem', textTransform: 'uppercase' }}>Streak</span>
            </div>
            <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>{profile?.streak || 0} Days</div>
          </div>

          <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#818cf8', marginBottom: '6px' }}>
              <Clock size={18} />
              <span style={{ fontSize: '0.8rem', textTransform: 'uppercase' }}>Hours</span>
            </div>
            <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>{profile?.total_hours || 0}h</div>
          </div>

          <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#34d399', marginBottom: '6px' }}>
              <FileText size={18} />
              <span style={{ fontSize: '0.8rem', textTransform: 'uppercase' }}>Resume</span>
            </div>
            <div style={{ fontSize: '1rem', fontWeight: '700', color: profile?.has_resume ? '#34d399' : '#9ca3af' }}>
              {profile?.has_resume ? 'Active' : 'Missing'}
            </div>
          </div>
        </div>

        {/* Target Role Editor */}
        <div style={{ paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)' }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '8px' }}>Career Target Role</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem', marginBottom: '1rem' }}>
            Changing your target role will dynamically re-benchmark your skill gaps and update recommended learning topics.
          </p>

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="input-field"
              style={{ width: 'auto', minWidth: '280px', backgroundColor: '#13182b', cursor: 'pointer' }}
            >
              {ROLE_CATEGORIES.map((cat) => (
                <optgroup key={cat.name} label={`${cat.icon} ${cat.name}`}>
                  {cat.roles.map((r) => (
                    <option key={r.name} value={r.name}>
                      {r.name}
                    </option>
                  ))}
                </optgroup>
              ))}
            </select>

            <button
              onClick={handleUpdateRole}
              disabled={updating || targetRole === profile?.target_role}
              className="btn-primary"
            >
              <span>{updating ? 'Updating...' : 'Save Role'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Logout Card */}
      <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1rem', marginBottom: '4px' }}>Sign Out</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem' }}>End your current learning session on this device.</p>
        </div>
        <button onClick={handleLogout} className="btn-secondary" style={{ color: '#f43f5e', borderColor: 'rgba(244, 63, 94, 0.3)' }}>
          <LogOut size={16} />
          <span>Log Out</span>
        </button>
      </div>
    </div>
  );
}
