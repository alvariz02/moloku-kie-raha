import Explorer from '../../components/Explorer';
export const metadata={title:'Jelajahi budaya'};
export default async function Page({searchParams}){const params=await searchParams;const initial=Object.fromEntries(['q','category','place','sort'].map(key=>[key,typeof params[key]==='string'?params[key]:'']));return <section className="chapter subpage"><span className="tag orange">ARSIP UNTUK SEMUA</span><h1 className="page-title">JELAJAHI<br/><span>WARISAN.</span></h1><p>Cari cerita yang membuatmu ingin mengenal Maluku Utara lebih dekat.</p><Explorer initial={initial}/></section>}
