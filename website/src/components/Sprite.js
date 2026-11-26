import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function Sprite({arquivo, legenda}) {
  const src = useBaseUrl(`/img/${arquivo}`);
  return (
    <figure>
      <img src={src} alt={legenda} />
      <figcaption>{legenda}</figcaption>
    </figure>
  );
}
