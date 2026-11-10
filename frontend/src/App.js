import { useEffect, useRef, useState } from "react";
import "@/App.css";
import axios from "axios";
import { AnimatePresence, motion } from "framer-motion";
import Lenis from "lenis";
import {
  ArrowUpRight,
  ChevronLeft,
  ChevronRight,
  Menu,
  Play,
  X,
} from "lucide-react";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
const fallback = {
  story: {
    eyebrow: "Arquivo não oficial · baseado em material divulgado",
    title: "Vice City nunca dorme.",
    intro:
      "Uma leitura editorial sobre o retorno ao estado de Leonida — onde cada pôr do sol esconde uma nova versão da verdade.",
    chapters: [],
  },
  characters: {
    items: [
      {
        id: "lucia",
        name: "Lucia",
        role: "A sobrevivente",
        color: "#ff2a6d",
        image:
          "https://images.unsplash.com/photo-1500305614571-ae5b6592e65d?auto=format&fit=crop&w=1000&q=85",
        bio: "Determinada, direta e pronta para recuperar o controle da própria história.",
      },
      {
        id: "jason",
        name: "Jason",
        role: "O cúmplice",
        color: "#05d9e8",
        image:
          "https://images.unsplash.com/photo-1669277752825-d7c26a392b4d?auto=format&fit=crop&w=1000&q=85",
        bio: "Jason conhece o risco de perto. Ao lado de Lucia, ele atravessa estradas costeiras.",
      },
    ],
  },
  easterEggs: {
    items: [
      {
        id: "loading-egg",
        title: "Pistas em carregamento",
        category: "PISTA",
        text: "O arquivo visual está sendo sincronizado.",
        x: 50,
        y: 50,
        image:
          "https://images.unsplash.com/photo-1593052289983-6c123686662c?auto=format&fit=crop&w=800&q=80",
      },
    ],
  },
  trailers: {
    items: [
      {
        id: "loading-trailer",
        number: "1",
        title: "Bem-vindos a Vice City",
        date: "ARQUIVO",
        image:
          "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=85",
        duration: "--:--",
      },
    ],
  },
};

const Reveal = ({ children, className = "", delay = 0 }) => (
  <motion.div
    className={className}
    initial={{ opacity: 0, y: 28 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-80px" }}
    transition={{ duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] }}
  >
    {children}
  </motion.div>
);

export default function App() {
  const [data, setData] = useState(fallback);
  const [menuOpen, setMenuOpen] = useState(false);
  const [character, setCharacter] = useState(0);
  const [eggFilter, setEggFilter] = useState("TODOS");
  const [trailer, setTrailer] = useState(0);
  const [apiOnline, setApiOnline] = useState(false);
  const storyRef = useRef(null),
    charactersRef = useRef(null),
    eggsRef = useRef(null),
    trailersRef = useRef(null);
  useEffect(() => {
    const lenis = new Lenis({ duration: 1.2, smoothWheel: true });
    let frame;
    const raf = (time) => {
      lenis.raf(time);
      frame = requestAnimationFrame(raf);
    };
    frame = requestAnimationFrame(raf);
    Promise.all([
      axios.get(`${API}/story`),
      axios.get(`${API}/characters`),
      axios.get(`${API}/easter-eggs`),
      axios.get(`${API}/trailers`),
    ])
      .then(([story, chars, eggs, trailers]) => {
        setData({
          story: story.data,
          characters: chars.data,
          easterEggs: eggs.data,
          trailers: trailers.data,
        });
        setApiOnline(true);
      })
      .catch(() => setApiOnline(false));
    return () => {
      cancelAnimationFrame(frame);
      lenis.destroy();
    };
  }, []);
  const scrollTo = (ref) => {
    setMenuOpen(false);
    ref.current?.scrollIntoView({ behavior: "smooth" });
  };
  const active = data.characters.items[character] || data.characters.items[0];
  const eggs = data.easterEggs.items.filter(
    (egg) => eggFilter === "TODOS" || egg.category === eggFilter,
  );
  const currentTrailer = data.trailers.items[trailer] || data.trailers.items[0];
  return (
    <main className="site-shell">
      <header className="topbar">
        <button
          className="menu-trigger"
          data-testid="hamburger-menu-button"
          onClick={() => setMenuOpen(true)}
        >
          <Menu size={20} />
          <span>MENU</span>
        </button>
        <a className="brand" data-testid="brand-link" href="#top">
          VC<span>VI</span>
        </a>
        <div className="api-status" data-testid="api-status">
          <i className={apiOnline ? "online" : ""}></i> API /{" "}
          {apiOnline ? "ONLINE" : "LOCAL"}
        </div>
      </header>
      <AnimatePresence>
        {menuOpen && (
          <motion.aside
            className="menu-panel"
            data-testid="hamburger-menu-panel"
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
          >
            <button
              className="close-menu"
              data-testid="close-menu-button"
              onClick={() => setMenuOpen(false)}
            >
              <X /> FECHAR
            </button>
            <p className="menu-kicker">DOSSIÊ 06 / 2025</p>
            <nav>
              <button
                data-testid="menu-story-link"
                onClick={() => scrollTo(storyRef)}
              >
                01 <span>HISTÓRIA</span>
                <ArrowUpRight />
              </button>
              <button
                data-testid="menu-characters-link"
                onClick={() => scrollTo(charactersRef)}
              >
                02 <span>PERSONAGENS</span>
                <ArrowUpRight />
              </button>
              <button
                data-testid="menu-eggs-link"
                onClick={() => scrollTo(eggsRef)}
              >
                03 <span>EASTER EGGS</span>
                <ArrowUpRight />
              </button>
              <button
                data-testid="menu-trailers-link"
                onClick={() => scrollTo(trailersRef)}
              >
                04 <span>TRAILERS</span>
                <ArrowUpRight />
              </button>
            </nav>
            <div className="menu-footer">
              LEONIDA STATE
              <br />
              26° 07&apos; N / 80° 11&apos; W
            </div>
          </motion.aside>
        )}
      </AnimatePresence>
      <section className="hero" id="top">
        <div className="hero-noise" />
        <div className="hero-copy">
          <p className="eyebrow reveal-line" data-testid="hero-eyebrow">
            GRAND THEFT AUTO VI / ARQUIVO EDITORIAL
          </p>
          <h1 data-testid="hero-title">
            <span>WELCOME</span>
            <span>
              TO <em>VICE</em> CITY
            </span>
          </h1>
          <p className="hero-sub" data-testid="hero-description">
            Uma história de crime, desejo e sobrevivência sob o sol de Leonida.
          </p>
          <button
            className="scroll-cue"
            data-testid="hero-scroll-button"
            onClick={() => scrollTo(storyRef)}
          >
            EXPLORAR O DOSSIÊ <ArrowUpRight size={16} />
          </button>
        </div>
        <div className="hero-figure">
          <img
            data-testid="hero-image"
            src="https://images.unsplash.com/photo-1779333429848-d6494e6b11ff?auto=format&fit=crop&w=1200&q=85"
            alt="Noite tropical em Vice City"
          />
          <div className="hero-stamp">
            VI
            <br />
            <small>
              THE
              <br />
              DOSSIER
            </small>
          </div>
        </div>
        <div className="hero-index">
          01 <span>/</span> 04
        </div>
      </section>
      <div className="marquee" data-testid="editorial-marquee">
        <span>NO ONE GETS OUT CLEAN</span>
        <b>✶</b>
        <span>NO ONE GETS OUT CLEAN</span>
        <b>✶</b>
        <span>NO ONE GETS OUT CLEAN</span>
      </div>
      <section
        className="story section-wrap"
        ref={storyRef}
        data-testid="story-section"
      >
        <Reveal>
          <p className="section-label">01 / A NARRATIVA</p>
          <div className="section-heading">
            <h2>{data.story.title}</h2>
            <p>{data.story.intro}</p>
          </div>
        </Reveal>
        <div className="chapters">
          {data.story.chapters.map((chapter, index) => (
            <Reveal key={chapter.number} delay={index * 0.08}>
              <article
                className="chapter"
                data-testid={`story-chapter-${chapter.number}`}
              >
                <div className="chapter-number">{chapter.number}</div>
                <div>
                  <span
                    className={`tag ${chapter.tag === "TEORIA" ? "theory" : ""}`}
                  >
                    {chapter.tag}
                  </span>
                  <h3>{chapter.title}</h3>
                  <p>{chapter.text}</p>
                </div>
                <ArrowUpRight className="chapter-arrow" />
              </article>
            </Reveal>
          ))}
        </div>
      </section>
      <section
        className="characters section-wrap"
        ref={charactersRef}
        data-testid="characters-section"
      >
        <Reveal>
          <p className="section-label">02 / OS DOIS LADOS</p>
          <div className="characters-intro">
            <h2>
              PARCEIROS
              <br />
              <i>OU PRESAS?</i>
            </h2>
            <p>
              Escolha um personagem para entrar na história. Mais nomes serão
              adicionados conforme o arquivo crescer.
            </p>
          </div>
        </Reveal>
        <div
          className="character-stage"
          style={{ "--character-color": active.color }}
        >
          <AnimatePresence mode="wait">
            <motion.img
              key={active.id}
              data-testid="active-character-image"
              src={active.image}
              alt={active.name}
              initial={{ opacity: 0, scale: 1.04 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.45 }}
            />
          </AnimatePresence>
          <div className="character-name" data-testid="active-character-name">
            {active.name}
          </div>
          <div className="character-meta">
            <span>{active.role}</span>
            <p>{active.bio}</p>
          </div>
        </div>
        <div className="character-switcher">
          {data.characters.items.map((item, index) => (
            <button
              key={item.id}
              data-testid={`character-switch-${item.id}`}
              className={character === index ? "active" : ""}
              onClick={() => setCharacter(index)}
            >
              <img src={item.image} alt={item.name} />
              <span>0{index + 1}</span>
              <strong>{item.name}</strong>
            </button>
          ))}
          <button
            className="future-character"
            data-testid="future-character-button"
            onClick={() =>
              alert("Novos personagens entram no arquivo em breve.")
            }
          >
            ＋<span>EM BREVE</span>
          </button>
        </div>
      </section>
      <section
        className="eggs section-wrap"
        ref={eggsRef}
        data-testid="easter-eggs-section"
      >
        <Reveal>
          <p className="section-label">03 / PISTAS ESCONDIDAS</p>
          <div className="section-heading">
            <h2>Olhe duas vezes.</h2>
            <p>
              Detalhes que passam rápido demais para serem acaso. Explore o mapa
              visual e filtre entre pistas confirmadas e teorias.
            </p>
          </div>
        </Reveal>
        <div className="egg-filters">
          {["TODOS", "CIDADE", "PISTA", "TEORIA"].map((filter) => (
            <button
              key={filter}
              data-testid={`egg-filter-${filter.toLowerCase()}`}
              className={eggFilter === filter ? "active" : ""}
              onClick={() => setEggFilter(filter)}
            >
              {filter}
            </button>
          ))}
        </div>
        <div className="egg-map" data-testid="easter-egg-map">
          <div className="map-grid" />
          {eggs.map((egg, index) => (
            <motion.button
              layout
              key={egg.id}
              data-testid={`easter-egg-marker-${egg.id}`}
              className="egg-marker"
              style={{ left: `${egg.x}%`, top: `${egg.y}%` }}
              onClick={() =>
                document
                  .getElementById(`egg-card-${egg.id}`)
                  ?.scrollIntoView({ behavior: "smooth", block: "center" })
              }
            >
              <span>0{index + 1}</span>
            </motion.button>
          ))}
        </div>
        <div className="egg-cards">
          {eggs.map((egg) => (
            <Reveal key={egg.id}>
              <article
                id={`egg-card-${egg.id}`}
                className="egg-card"
                data-testid={`easter-egg-card-${egg.id}`}
              >
                <img src={egg.image} alt="" />
                <div>
                  <span className="tag">{egg.category}</span>
                  <h3>{egg.title}</h3>
                  <p>{egg.text}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>
      <section
        className="trailers section-wrap"
        ref={trailersRef}
        data-testid="trailers-section"
      >
        <Reveal>
          <p className="section-label">04 / MOVING PICTURES</p>
          <div className="trailer-heading">
            <h2>
              O trailer
              <br />
              <i>continua.</i>
            </h2>
            <div className="trailer-controls">
              <button
                data-testid="trailer-previous-button"
                onClick={() =>
                  setTrailer(
                    (trailer - 1 + data.trailers.items.length) %
                      data.trailers.items.length,
                  )
                }
              >
                <ChevronLeft />
              </button>
              <button
                data-testid="trailer-next-button"
                onClick={() =>
                  setTrailer((trailer + 1) % data.trailers.items.length)
                }
              >
                <ChevronRight />
              </button>
            </div>
          </div>
        </Reveal>
        <div className="trailer-card">
          <img
            data-testid="active-trailer-image"
            src={currentTrailer.image}
            alt={currentTrailer.title}
          />
          <div className="trailer-overlay">
            <div>
              <span>{currentTrailer.date}</span>
              <h3>{currentTrailer.title}</h3>
            </div>
            <button
              data-testid="trailer-play-button"
              onClick={() =>
                alert("Trailer em destaque: material oficial da Rockstar.")
              }
            >
              <Play fill="currentColor" size={18} />
              <span>ASSISTIR / {currentTrailer.duration}</span>
            </button>
          </div>
        </div>
        <div className="trailer-progress">
          <span>0{Number(currentTrailer.number)}</span>
          <div>
            <i
              style={{
                width: `${((trailer + 1) / data.trailers.items.length) * 100}%`,
              }}
            />
          </div>
          <span>0{data.trailers.items.length}</span>
        </div>
      </section>
      <footer data-testid="site-footer">
        <span>VCVI / DOSSIÊ 2025</span>
        <span>UMA CARTA DE AMOR A LEONIDA</span>
        <a href="#top" data-testid="back-to-top-link">
          VOLTAR AO TOPO ↑
        </a>
      </footer>
    </main>
  );
}
