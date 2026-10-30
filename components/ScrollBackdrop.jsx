'use client';
import {useEffect,useRef} from 'react';
import {usePathname} from 'next/navigation';
import {LeafSprig,Contours} from './NatureArt';
import {frameAt,FRAME_COLUMNS,FRAME_ROWS} from '../lib/scroll-frames.mjs';

// Twelve distinct animation frames, sampled from one atlas in reading order.
export default function ScrollBackdrop(){
 const path=usePathname();
 const stage=useRef(null);
 const canvasRef=useRef(null);
 useEffect(()=>{
  const root=stage.current;
  const canvas=canvasRef.current;
  const ctx=canvas.getContext('2d',{alpha:false});
  if(!ctx)return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const atlas=new Image();
  let raf=0,disposed=false,ready=false;
  function paintFrame(index,alpha){
   const w=atlas.naturalWidth/FRAME_COLUMNS;
   const h=atlas.naturalHeight/FRAME_ROWS;
   const scale=Math.max(canvas.width/w,canvas.height/h);
   const width=w*scale,height=h*scale;
   ctx.globalAlpha=alpha;
   ctx.drawImage(atlas,(index%FRAME_COLUMNS)*w,Math.floor(index/FRAME_COLUMNS)*h,w,h,(canvas.width-width)/2,(canvas.height-height)/2,width,height);
  }
  function draw(){
   raf=0;
   if(disposed||!ready||document.hidden)return;
   const total=Math.max(1,document.documentElement.scrollHeight-innerHeight);
   const progress=Math.min(1,Math.max(0,scrollY/total));
   const frame=frameAt(progress,reduce.matches);
   paintFrame(frame.index,1);
   if(frame.blend>0)paintFrame(frame.next,frame.blend);
   ctx.globalAlpha=1;
   root.dataset.frame=String(frame.index);
   root.dataset.frameCount='12';
   root.dataset.scrollProgress=progress.toFixed(3);
   root.classList.add('frames-ready');
  }
  function schedule(){if(!raf&&!disposed)raf=requestAnimationFrame(draw);}
  function resize(){const ratio=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(innerWidth*ratio);canvas.height=Math.round(innerHeight*ratio);ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';schedule();}
  atlas.onload=()=>{if(disposed)return;ready=true;resize()};
  atlas.src='/assets/culture-sequence/atlas.png';
  const observer=new ResizeObserver(schedule);
  const main=document.querySelector('main');if(main)observer.observe(main);
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',resize);
  addEventListener('pageshow',schedule);
  document.addEventListener('visibilitychange',schedule);
  reduce.addEventListener('change',schedule);
  resize();
  return()=>{disposed=true;atlas.onload=null;cancelAnimationFrame(raf);observer.disconnect();removeEventListener('scroll',schedule);removeEventListener('resize',resize);removeEventListener('pageshow',schedule);document.removeEventListener('visibilitychange',schedule);reduce.removeEventListener('change',schedule)};
 },[path]);
 return <div ref={stage} className="backdrop frame-backdrop" aria-hidden="true"><img className="frame-fallback" src="/assets/maluku.jpg" alt=""/><canvas ref={canvasRef}/><div className="frame-shade"/><Contours/><LeafSprig className="backdrop-leaf"/></div>;
}
