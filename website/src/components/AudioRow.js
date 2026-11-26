import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function AudioRow({nome, arquivo}) {
  const src = useBaseUrl(`/audio/${arquivo}`);
  return (
    <div className="audio-row">
      <span>{nome}</span>
      <audio controls preload="none" src={src} />
    </div>
  );
}
