'use client';
import Link from 'next/link';
import {usePathname} from 'next/navigation';
import {useEffect,useState} from 'react';
import ScrollBackdrop from './ScrollBackdrop';
import {SpiceMark} from './SpiceIdentity';
import ExperienceMotion from './ExperienceMotion';
function NavIcon({index}){const paths=['M3 11 12 3l9 8M6 9v12h12V9M10 21v-7h4v7','m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Zm6-3v15m6-12v15','M4 4h16v16H4zM4 16l5-5 4 4 3-3 4 4M15 8h.01','M20 5a5 5 0 0 0-8 1 5 5 0 0 0-8-1c-4 5 2 10 8 15 6-5 12-10 8-15Z','M9 8a3 3 0 1 1 5 2c-2 1-2 2-2 4M12 18h.01M4 3h16v18H4z'];return <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={paths[index]}/></svg>}
const links=[['/','⌂','Pembuka'],['/jelajahi','◇','Jelajahi'],['/galeri','▧','Galeri'],['/favorit','♡','Favorit'],['/kuis','✳','Kuis']];
export default function Shell({children}){const path=usePathname();const [progress,setProgress]=useState(0);useEffect(()=>{const update=()=>{const total=document.documentElement.scrollHeight-innerHeight;setProgress(total>0?scrollY/total*100:0)};update();addEventListener('scroll',update,{passive:true});return()=>removeEventListener('scroll',update)},[path]);return <><a className="skip" href="#main-content">Lewati navigasi</a><ScrollBackdrop/><ExperienceMotion/><div className="progress" style={{width:`${progress}%`}}/><header><Link className="brand" href="/"><span className="brand-symbol"><SpiceMark/></span><span className="brand-name">MOLOKU<small>BUDAYA MALUKU UTARA</small></span></Link><Link className="header-link" href="/jelajahi">Buka koleksi ↗</Link></header><main id="main-content" key={path}>{children}</main><nav className="dock" aria-label="Navigasi utama">{links.map(([url,icon,title],index)=><Link key={url} href={url} aria-current={path===url?'page':undefined}><span aria-hidden="true"><NavIcon index={index}/></span>{title}</Link>)}</nav></>}
