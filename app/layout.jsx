import './globals.css';
import 'lenis/dist/lenis.css';
import './elegant.css';
import './nature.css';
import './moloku-modern.css';
import Shell from '../components/Shell';
export const metadata={title:{default:'MOLOKU — Cerita dari Timur',template:'%s | MOLOKU'},description:'Ruang eksplorasi budaya Maluku Utara: cerita, koleksi, galeri, favorit, dan kuis.'};
export default function Layout({children}){return <html lang="id"><body><Shell>{children}</Shell></body></html>}
