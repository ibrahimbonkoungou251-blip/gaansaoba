const hotelsData = [
  {
    id: 1,
    name: "Hôtel Faso Luxe",
    type: "hotel",
    stars: 5,
    location: "Ouagadougou - Centre Ville",
    city: "ouaga",
    price: 45000,
    image: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?q=80&w=1200",
    amenities: ["🏊", "📶", "❄️", "🍴", "🅿️"],
    tag: "Populaire",
    phone: "+226 70 00 00 00",
    email: "contact@fasoluxe.com"
  },
  {
    id: 2,
    name: "Auberge Wend Panga",
    type: "auberge",
    stars: 3,
    location: "Bobo-Dioulasso - Quartier Latin",
    city: "bobo",
    price: 12000,
    image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=1200",
    amenities: ["📶", "❄️", "🅿️"],
    tag: "Économique",
    phone: "+226 65 11 11 11",
    email: "auberge@wendpanga.com"
  },
  {
    id: 3,
    name: "Hôtel Sahel Prestige",
    type: "hotel",
    stars: 4,
    location: "Ouahigouya - Secteur 1",
    city: "ouahi",
    price: 30000,
    image: "https://images.unsplash.com/photo-1566665797739-1674de7a421a?q=80&w=1200",
    amenities: ["📶", "❄️", "🍴", "🅿️", "💼"],
    tag: "Affaires",
    phone: "+226 76 22 22 22",
    email: "reservation@sahelprestige.com"
  },
  {
    id: 4,
    name: "La Résidence du Parc",
    type: "residence",
    stars: 4,
    location: "Ouagadougou - Ouaga 2000",
    city: "ouaga",
    price: 55000,
    image: "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1200",
    amenities: ["🏊", "📶", "❄️", "🍳", "🅿️"],
    tag: "Luxe",
    phone: "+226 78 33 33 33",
    email: "residence@parc.bf"
  },
  {
    id: 5,
    name: "Hôtel Silmandé",
    type: "hotel",
    stars: 4,
    location: "Ouagadougou - Zone du Bois",
    city: "ouaga",
    price: 65000,
    image: "https://images.unsplash.com/photo-1564501049412-61c2a3083791?q=80&w=1200",
    amenities: ["🏊", "📶", "❄️", "🍴", "🎾", "🅿️"],
    tag: "Premium",
    phone: "+226 25 35 60 60",
    email: "silmande@sopatel.bf"
  },
  {
    id: 6,
    name: "Auberge de la Paix",
    type: "auberge",
    stars: 2,
    location: "Banfora - Centre",
    city: "banfora",
    price: 8500,
    image: "https://images.unsplash.com/photo-1561501900-3701fa6a0864?q=80&w=1200",
    amenities: ["📶", "🅿️", "🌳"],
    tag: "Nature",
    phone: "+226 60 55 55 55",
    email: "paix@banfora.com"
  }
];

const promotions = [
  {
    id: 1,
    title: "Spécial Weekend à Bobo",
    discount: "-20%",
    description: "Profitez d'un séjour à Bobo-Dioulasso à prix réduit tout ce weekend.",
    image: "https://images.unsplash.com/photo-1596436889106-be35e843f974?q=80&w=1200"
  },
  {
    id: 2,
    title: "Offre Famille Ouaga 2000",
    discount: "-15%",
    description: "Réservez 3 nuits et la 4ème est à moitié prix pour toute la famille.",
    image: "https://images.unsplash.com/photo-1540541338287-41700207dee6?q=80&w=1200"
  }
];

const testimonials = [
  {
    name: "Idrissa Traoré",
    role: "Voyageur d'affaires",
    text: "Gaansaoba a simplifié mes déplacements professionnels au Burkina. Je réserve en 2 minutes et le paiement par Orange Money est ultra pratique.",
    avatar: "👤"
  },
  {
    name: "Fatoumata Ouédraogo",
    role: "Touriste",
    text: "Superbe plateforme ! J'ai pu comparer les prix des auberges à Banfora et trouver la perle rare pour mes vacances.",
    avatar: "👤"
  },
  {
    name: "Jean-Pierre Blanc",
    role: "Expatrié",
    text: "La qualité des photos et les informations sur les services sont très fiables. C'est le Booking.com du Burkina !",
    avatar: "👤"
  }
];
