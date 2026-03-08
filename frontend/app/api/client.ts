export type ScriptInputMode = 'text' | 'screenplay';
export type RenderMode = 'draft' | 'standard' | 'high-quality';
export type JobStatus = 'queued' | 'rendering' | 'complete' | 'failed';

export interface Project {
  id: string;
  name: string;
  scriptInputMode: ScriptInputMode;
  initialScript: string;
  createdAt: string;
}

export interface Shot {
  id: string;
  label: string;
  durationSeconds: number;
  prompt: string;
}

export interface Scene {
  id: string;
  title: string;
  summary: string;
  shots: Shot[];
}

export interface RenderJob {
  id: string;
  projectId: string;
  status: JobStatus;
  progressPercent: number;
  mode: RenderMode;
  message?: string;
}

export interface TimelineSettings {
  sceneOrder: string[];
  clipDurationSeconds: number;
  subtitlesEnabled: boolean;
  voiceVolume: number;
  musicVolume: number;
}

export interface ProviderStatus {
  provider: 'openai' | 'elevenlabs' | 'runway';
  available: boolean;
  guidance: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {})
    },
    cache: 'no-store'
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export const apiClient = {
  createProject(payload: Pick<Project, 'name' | 'scriptInputMode' | 'initialScript'>) {
    return request<Project>('/projects', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },
  getProject(projectId: string) {
    return request<Project>(`/projects/${projectId}`);
  },
  getScenes(projectId: string) {
    return request<Scene[]>(`/projects/${projectId}/scenes`);
  },
  updateShotPrompt(projectId: string, sceneId: string, shotId: string, prompt: string) {
    return request<Scene>(`/projects/${projectId}/scenes/${sceneId}/shots/${shotId}`, {
      method: 'PATCH',
      body: JSON.stringify({ prompt })
    });
  },
  enqueueRender(projectId: string, mode: RenderMode) {
    return request<RenderJob>(`/projects/${projectId}/render`, {
      method: 'POST',
      body: JSON.stringify({ mode })
    });
  },
  getRenderJobs(projectId: string) {
    return request<RenderJob[]>(`/projects/${projectId}/renders`);
  },
  updateTimeline(projectId: string, settings: TimelineSettings) {
    return request<TimelineSettings>(`/projects/${projectId}/timeline`, {
      method: 'PUT',
      body: JSON.stringify(settings)
    });
  },
  getProviderStatuses() {
    return request<ProviderStatus[]>('/providers/status');
  },
  getExportLinks(projectId: string) {
    return request<Record<'mp4' | 'json' | 'srt' | 'wav' | 'prompts', string>>(
      `/projects/${projectId}/exports`
    );
  }
};
