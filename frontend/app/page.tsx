import { ProjectCreateForm } from '@/components/ProjectCreateForm';
import { ProviderStatusNotice } from '@/components/ProviderStatusNotice';

export default function ProjectCreatePage() {
  return (
    <main className="container grid">
      <h1>Create Video Project</h1>
      <ProviderStatusNotice />
      <ProjectCreateForm />
    </main>
  );
}
