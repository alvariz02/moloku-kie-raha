import Explorer from '../../components/Explorer';
export const metadata={title:'Koleksi favorit'};
export default function Page(){return <section className="chapter subpage"><span className="tag pink">RUANG PRIBADIMU</span><h1 className="page-title">CERITA<br/><span>FAVORIT.</span></h1><p>Koleksi pilihanmu disimpan di browser perangkat ini.</p><Explorer favorites/></section>}
