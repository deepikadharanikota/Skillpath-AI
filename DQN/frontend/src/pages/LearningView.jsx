import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { 
  Play, 
  CheckCircle2, 
  Lock, 
  Sparkles, 
  RefreshCw, 
  AlertCircle, 
  ArrowRight,
  Tv,
  Clock,
  Eye,
  Check
} from 'lucide-react';
import { api } from '../api';

const DEFAULT_MODULES = [
  { key: 'intro', fallbackLabel: '1. Fundamentals', icon: '🌱' },
  { key: 'core', fallbackLabel: '2. Core Concepts', icon: '🔥' },
  { key: 'advanced', fallbackLabel: '3. Advanced Concepts', icon: '⚡' },
  { key: 'summary', fallbackLabel: '4. Integration & Review', icon: '🎓' }
];

export default function LearningView() {
  const { topicId } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const currentTopic = decodeURIComponent(topicId || 'Machine Learning');
  const currentModule = searchParams.get('module') || 'intro';

  const [videoData, setVideoData] = useState(null);
  const [activeVideo, setActiveVideo] = useState(null);
  const [completingVideoId, setCompletingVideoId] = useState(null);
  const [resumeSeconds, setResumeSeconds] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadVideos = async () => {
    setLoading(true);
    setError('');
    try {
      // 1. Switch server state to this topic & module
      await api.navigateTopic(currentTopic, currentModule);
      // 2. Fetch videos & gating status
      const data = await api.getVideos(currentTopic, currentModule);
      setVideoData(data);

      const targetVideoParam = searchParams.get('video');
      const targetTimeParam = parseFloat(searchParams.get('t') || '0');

      const modVids = (data.videos || []).filter(v => v.module === currentModule);
      
      let matchedVideo = null;
      let startPos = 0;

      if (targetVideoParam) {
        matchedVideo = (data.videos || []).find(v => (v.id === targetVideoParam || v.url === targetVideoParam || v.url?.includes(targetVideoParam)));
        startPos = targetTimeParam;
      } else if (data.last_video_id) {
        matchedVideo = (data.videos || []).find(v => (v.id === data.last_video_id || v.url === data.last_video_id || v.url?.includes(data.last_video_id)));
        startPos = parseFloat(data.last_video_position_seconds || 0);
      }

      if (!matchedVideo) {
        matchedVideo = modVids.find(v => v.recommended) || modVids[0] || (data.videos || [])[0];
      }

      setActiveVideo(matchedVideo);
      setResumeSeconds(startPos);

      // Persist active video on load
      if (matchedVideo) {
        api.saveLearningPosition(
          currentTopic,
          currentModule,
          matchedVideo.id || matchedVideo.url,
          startPos,
          matchedVideo.title
        ).catch(() => {});
      }
    } catch (err) {
      console.error('Failed to load videos:', err);
      setError(err.message || 'Error loading course videos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadVideos();
  }, [currentTopic, currentModule]);

  const handleModuleChange = (modKey) => {
    setSearchParams({ module: modKey });
  };

  const handleSelectVideo = (video) => {
    setActiveVideo(video);
    setResumeSeconds(0);
    api.saveLearningPosition(
      currentTopic,
      currentModule,
      video.id || video.url,
      0,
      video.title
    ).catch(() => {});
  };

  const handleMarkVideoCompleted = async (video) => {
    const videoId = video.id || video.url;
    setCompletingVideoId(videoId);
    try {
      const res = await api.completeVideo(currentTopic, currentModule, videoId);
      // Update local state directly
      if (videoData) {
        const updatedVideos = (videoData.videos || []).map(v => {
          if ((v.id || v.url) === videoId) {
            return { ...v, is_completed: true };
          }
          return v;
        });
        setVideoData({
          ...videoData,
          videos: updatedVideos,
          completed_count: res.completed_count,
          is_quiz_unlocked: res.is_quiz_unlocked,
          course_progress: res.course_progress || videoData.course_progress
        });
      }
    } catch (err) {
      console.error('Failed to complete video:', err);
    } finally {
      setCompletingVideoId(null);
    }
  };

  const getEmbedUrl = (url, startSec = 0) => {
    if (!url) return '';
    let vidId = '';
    if (url.includes('v=')) {
      vidId = url.split('v=')[1]?.split('&')[0];
    } else if (url.includes('youtu.be/')) {
      vidId = url.split('youtu.be/')[1]?.split('?')[0];
    }
    if (!vidId) return '';
    let embed = `https://www.youtube.com/embed/${vidId}?autoplay=0`;
    if (startSec && startSec > 0) {
      embed += `&start=${Math.floor(startSec)}`;
    }
    return embed;
  };

  const isUnlocked = videoData?.is_quiz_unlocked;
  const completedCount = videoData?.completed_count || 0;
  const requiredCount = videoData?.required_count || 1;

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <RefreshCw size={36} color="#818cf8" style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  const currentModuleVideos = (videoData?.videos || []).filter(v => v.module === currentModule);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Topic Header & Breadcrumb */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>Learning Center &gt;</span>
            <span style={{ fontSize: '0.86rem', color: '#818cf8', fontWeight: '600' }}>{currentTopic}</span>
          </div>
          <h1 style={{ fontSize: '2.2rem' }}>{currentTopic}</h1>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="badge badge-indigo" style={{ padding: '6px 14px', fontSize: '0.85rem' }}>
            Adapted Level: {videoData?.current_difficulty?.toUpperCase() || 'BEGINNER'}
          </span>
        </div>
      </div>

      {/* Course Progress Summary Bar */}
      {videoData?.course_progress && (
        <div className="glass-card" style={{
          padding: '14px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1.25rem',
          flexWrap: 'wrap',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          background: 'rgba(99, 102, 241, 0.04)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontWeight: '600', fontSize: '0.95rem' }}>Course Progress:</span>
            <span style={{ color: '#818cf8', fontWeight: '700', fontSize: '1.1rem' }}>
              {videoData.course_progress.percentage}%
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-dim)' }}>
              ({videoData.course_progress.completed_modules} of 4 Modules Completed)
            </span>
          </div>
          <div style={{ width: '240px' }} className="progress-track">
            <div 
              className={`progress-fill ${videoData.course_progress.is_completed ? 'progress-fill-emerald' : ''}`}
              style={{ width: `${videoData.course_progress.percentage}%` }} 
            />
          </div>
        </div>
      )}

      {error && (
        <div style={{
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          padding: '1rem',
          borderRadius: '12px',
          color: '#fca5a5',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Module Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        borderBottom: '1px solid var(--border-color)',
        paddingBottom: '8px',
        overflowX: 'auto'
      }}>
        {DEFAULT_MODULES.map((m) => {
          const isActive = currentModule === m.key;
          const syllabusMod = videoData?.syllabus?.modules?.[m.key];
          const displayLabel = syllabusMod?.title || m.fallbackLabel;
          return (
            <button
              key={m.key}
              onClick={() => handleModuleChange(m.key)}
              style={{
                background: isActive ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%)' : 'transparent',
                border: isActive ? '1px solid rgba(99, 102, 241, 0.4)' : '1px solid transparent',
                borderRadius: '10px',
                padding: '10px 18px',
                color: isActive ? '#fff' : 'var(--text-muted)',
                fontWeight: isActive ? '700' : '500',
                fontSize: '0.92rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                whiteSpace: 'nowrap'
              }}
            >
              <span>{m.icon}</span>
              <span>{displayLabel}</span>
            </button>
          );
        })}
      </div>

      {/* Module Syllabus & Objectives */}
      {videoData?.syllabus?.modules?.[currentModule] && (
        <div className="glass-card" style={{
          padding: '1.25rem 1.5rem',
          background: 'rgba(99, 102, 241, 0.04)',
          border: '1px solid rgba(99, 102, 241, 0.2)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', flexWrap: 'wrap', gap: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Sparkles size={18} color="#818cf8" />
              <span style={{ fontWeight: '700', fontSize: '1rem', color: '#fff' }}>
                {videoData.syllabus.modules[currentModule].title}
              </span>
            </div>
            {videoData.syllabus.modules[currentModule].focus && (
              <span className="badge badge-indigo" style={{ fontSize: '0.78rem' }}>
                Focus: {videoData.syllabus.modules[currentModule].focus}
              </span>
            )}
          </div>
          {videoData.syllabus.modules[currentModule].subtopics?.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
              {videoData.syllabus.modules[currentModule].subtopics.map((sub, idx) => (
                <div key={idx} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  backgroundColor: 'rgba(255, 255, 255, 0.04)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '20px',
                  padding: '4px 12px',
                  fontSize: '0.82rem',
                  color: '#e2e8f0'
                }}>
                  <span style={{ color: '#818cf8', fontWeight: 'bold' }}>•</span>
                  <span>{sub}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ── Main Content Area: Player on Left, Video List on Right ── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 380px', gap: '1.75rem' }}>
        {/* Left Column: Active Video Player & Gated Quiz Card */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {activeVideo ? (
            <div className="glass-card" style={{ padding: '1.5rem' }}>
              {resumeSeconds > 0 && (
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '8px',
                  backgroundColor: 'rgba(99, 102, 241, 0.15)',
                  border: '1px solid rgba(99, 102, 241, 0.35)',
                  borderRadius: '20px',
                  padding: '4px 12px',
                  fontSize: '0.8rem',
                  color: '#c7d2fe',
                  marginBottom: '12px'
                }}>
                  <Play size={12} fill="#818cf8" color="#818cf8" />
                  <span>Resuming playback from <strong>{Math.floor(resumeSeconds / 60)}:{String(Math.floor(resumeSeconds % 60)).padStart(2, '0')}</strong></span>
                </div>
              )}

              {/* Embedded Player */}
              <div style={{
                position: 'relative',
                paddingBottom: '56.25%',
                height: 0,
                borderRadius: '14px',
                overflow: 'hidden',
                backgroundColor: '#000',
                marginBottom: '1rem'
              }}>
                {getEmbedUrl(activeVideo.url, resumeSeconds) ? (
                  <iframe
                    src={getEmbedUrl(activeVideo.url, resumeSeconds)}
                    title={activeVideo.title}
                    style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 0 }}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                ) : (
                  <div style={{ position: 'absolute', top: '45%', left: '35%', color: 'var(--text-muted)' }}>
                    Video stream available on YouTube
                  </div>
                )}
              </div>

              {/* Video Title & Actions */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                <div style={{ flex: 1, minWidth: '240px' }}>
                  <h2 style={{ fontSize: '1.25rem', marginBottom: '6px' }}>{activeVideo.title}</h2>
                  <div style={{ display: 'flex', gap: '14px', fontSize: '0.84rem', color: 'var(--text-dim)' }}>
                    <span>📺 {activeVideo.channel}</span>
                    <span>⏱ {activeVideo.duration}</span>
                    <span>👁 {activeVideo.views} views</span>
                  </div>
                </div>

                {/* Mark as Watched Button */}
                <button
                  onClick={() => handleMarkVideoCompleted(activeVideo)}
                  disabled={activeVideo.is_completed || completingVideoId === (activeVideo.id || activeVideo.url)}
                  className={activeVideo.is_completed ? 'btn-emerald' : 'btn-primary'}
                  style={{ padding: '10px 18px', fontSize: '0.9rem' }}
                >
                  {activeVideo.is_completed ? (
                    <>
                      <CheckCircle2 size={16} />
                      <span>Watched & Completed</span>
                    </>
                  ) : (
                    <>
                      <Check size={16} />
                      <span>{completingVideoId === (activeVideo.id || activeVideo.url) ? 'Recording...' : 'Mark as Watched'}</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          ) : (
            <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
              <Tv size={48} color="#9ca3af" style={{ margin: '0 auto 1rem' }} />
              <p style={{ color: 'var(--text-muted)' }}>No videos found for this module.</p>
            </div>
          )}

          {/* ── STRICT QUIZ GATING CARD ── */}
          <div className="glass-card" style={{
            padding: '2rem',
            border: isUnlocked 
              ? '1px solid rgba(16, 185, 129, 0.4)' 
              : '1px solid rgba(255, 255, 255, 0.08)',
            background: isUnlocked
              ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.06) 100%)'
              : 'var(--bg-card)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                  {isUnlocked ? (
                    <CheckCircle2 size={24} color="#10b981" />
                  ) : (
                    <Lock size={24} color="#f59e0b" />
                  )}
                  <h3 style={{ fontSize: '1.25rem' }}>
                    {isUnlocked ? '✓ Videos Completed — Quiz Unlocked!' : '🔒 Quiz Locked'}
                  </h3>
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                  {isUnlocked
                    ? `You have completed all required videos for this module. Challenge yourself with the 15-question adaptive quiz!`
                    : `Complete all required course videos (${completedCount}/${requiredCount} completed) to unlock the quiz.`}
                </p>
              </div>

              {/* Take Quiz Button */}
              {isUnlocked ? (
                <button
                  onClick={() => navigate(`/quiz/${encodeURIComponent(currentTopic)}?module=${encodeURIComponent(currentModule)}`)}
                  className="btn-emerald"
                  style={{ padding: '14px 28px', fontSize: '1rem', fontWeight: '700' }}
                >
                  <Sparkles size={18} />
                  <span>Start 15 Question Quiz</span>
                </button>
              ) : (
                <button
                  disabled
                  className="btn-primary"
                  style={{ opacity: 0.5, cursor: 'not-allowed', padding: '12px 24px' }}
                >
                  <Lock size={16} />
                  <span>Quiz Locked</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Module Videos Playlist */}
        <div className="glass-card" style={{ padding: '1.5rem', height: 'fit-content' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.05rem' }}>Module Videos</h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
              {completedCount}/{requiredCount} Watched
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {currentModuleVideos.map((video, idx) => {
              const isSelected = activeVideo && (activeVideo.id || activeVideo.url) === (video.id || video.url);
              return (
                <div
                  key={idx}
                  onClick={() => handleSelectVideo(video)}
                  style={{
                    display: 'flex',
                    gap: '12px',
                    padding: '10px',
                    borderRadius: '12px',
                    backgroundColor: isSelected ? 'rgba(99, 102, 241, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                    border: isSelected ? '1px solid rgba(99, 102, 241, 0.4)' : '1px solid var(--border-color)',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                >
                  {/* Thumbnail */}
                  <div style={{
                    width: '100px',
                    height: '60px',
                    borderRadius: '8px',
                    overflow: 'hidden',
                    backgroundColor: '#000',
                    flexShrink: 0,
                    position: 'relative'
                  }}>
                    {video.thumb ? (
                      <img src={video.thumb} alt={video.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    ) : (
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                        <Play size={18} color="#fff" />
                      </div>
                    )}
                    {video.is_completed && (
                      <div style={{
                        position: 'absolute',
                        top: '4px',
                        right: '4px',
                        backgroundColor: '#10b981',
                        borderRadius: '50%',
                        padding: '2px'
                      }}>
                        <Check size={12} color="#fff" />
                      </div>
                    )}
                  </div>

                  {/* Metadata */}
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{
                      fontSize: '0.85rem',
                      fontWeight: '600',
                      color: isSelected ? '#fff' : 'var(--text-main)',
                      lineHeight: '1.3',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      marginBottom: '4px'
                    }}>
                      {video.title}
                    </div>
                    <div style={{ fontSize: '0.74rem', color: 'var(--text-dim)', display: 'flex', gap: '8px' }}>
                      <span>⏱ {video.duration}</span>
                      {video.is_completed && <span style={{ color: '#10b981', fontWeight: '600' }}>✓ Watched</span>}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
