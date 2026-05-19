document.addEventListener('DOMContentLoaded', () => {
  // --- LOADER ---
  const loader = document.getElementById('loaderOverlay');
  setTimeout(() => {
    loader.style.opacity = '0';
    setTimeout(() => loader.style.display = 'none', 500);
  }, 1500);

  // --- HEADER SCROLL ---
  const header = document.getElementById('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // --- RENDER HOTELS ---
  const hotelsGrid = document.getElementById('hotelsGrid');
  if (hotelsGrid) {
    hotelsData.slice(0, 3).forEach(hotel => {
      const card = document.createElement('div');
      card.className = 'hotel-card';
      card.innerHTML = `
        <div class="hotel-img-wrapper">
          <img src="${hotel.image}" alt="${hotel.name}">
          <div class="hotel-tag">${hotel.tag}</div>
        </div>
        <div class="hotel-info">
          <div class="hotel-stars">${'⭐'.repeat(hotel.stars)}</div>
          <h3 class="hotel-name">${hotel.name}</h3>
          <p class="hotel-location">📍 ${hotel.location}</p>
          <div class="hotel-amenities">
            ${hotel.amenities.map(a => `<span class="amenity">${a}</span>`).join('')}
          </div>
          <div class="hotel-footer">
            <div class="hotel-price">${hotel.price.toLocaleString()} F CFA <span>/ nuit</span></div>
            <button class="btn-primary" onclick="openReservationModal(${hotel.id})">Réserver</button>
          </div>
        </div>
      `;
      hotelsGrid.appendChild(card);
    });
  }

  // --- RENDER PROMOTIONS ---
  const promosGrid = document.getElementById('promosGrid');
  if (promosGrid) {
    promotions.forEach(promo => {
      const card = document.createElement('div');
      card.className = 'promo-card'; // Style to be added if needed or reuse existing
      card.style.cssText = `
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url(${promo.image}) center/cover;
        border-radius: 20px; padding: 40px; color: white; min-height: 250px;
        display: flex; flex-direction: column; justify-content: flex-end;
      `;
      card.innerHTML = `
        <div class="promo-discount" style="background: var(--secondary); color: black; padding: 5px 15px; border-radius: 50px; align-self: flex-start; font-weight: 800; margin-bottom: 15px;">${promo.discount}</div>
        <h3 style="font-size: 1.8rem; margin-bottom: 10px;">${promo.title}</h3>
        <p style="opacity: 0.8; margin-bottom: 20px;">${promo.description}</p>
        <a href="promotions.html" class="btn-outline" style="width: fit-content; border-color: white;">En profiter →</a>
      `;
      promosGrid.appendChild(card);
    });
  }

  // --- RENDER TESTIMONIALS ---
  const testimonialsTrack = document.getElementById('testimonialsTrack');
  const testimonialsDots = document.getElementById('testimonialsDots');
  if (testimonialsTrack) {
    testimonials.forEach((t, i) => {
      const slide = document.createElement('div');
      slide.className = 'testimonial-slide';
      slide.style.cssText = `
        min-width: 100%; padding: 40px; text-align: center;
      `;
      slide.innerHTML = `
        <div class="t-avatar" style="font-size: 3rem; margin-bottom: 20px;">${t.avatar}</div>
        <p class="t-text" style="font-size: 1.2rem; font-style: italic; margin-bottom: 20px; max-width: 800px; margin-left: auto; margin-right: auto;">"${t.text}"</p>
        <h4 class="t-name" style="font-weight: 700; color: var(--primary);">${t.name}</h4>
        <p class="t-role" style="font-size: 0.9rem; opacity: 0.6;">${t.role}</p>
      `;
      testimonialsTrack.appendChild(slide);

      const dot = document.createElement('div');
      dot.className = `dot ${i === 0 ? 'active' : ''}`;
      dot.style.cssText = `
        width: 10px; height: 10px; background: #ddd; border-radius: 50%; cursor: pointer; transition: 0.3s;
      `;
      if(i === 0) dot.style.background = 'var(--primary)';
      testimonialsDots.appendChild(dot);
    });
  }

  // --- SEARCH TABS ---
  const searchTabs = document.querySelectorAll('.search-tab');
  searchTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      searchTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  // --- STATS COUNTER ---
  const stats = document.querySelectorAll('.stat-number');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.getAttribute('data-count'));
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
          current += increment;
          if (current >= target) {
            entry.target.innerText = target;
            clearInterval(timer);
          } else {
            entry.target.innerText = Math.floor(current);
          }
        }, 30);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  stats.forEach(s => observer.observe(s));

  // --- MODAL LOGIC ---
  const modal = document.getElementById('reservationModal');
  const closeBtn = document.getElementById('modalClose');
  const resForm = document.getElementById('reservationForm');
  const successModal = document.getElementById('successModal');

  window.openReservationModal = (hotelId) => {
    const hotel = hotelsData.find(h => h.id === hotelId);
    if (hotel) {
      document.getElementById('modalHotelName').innerText = hotel.name;
      document.getElementById('totalPrice').innerText = hotel.price.toLocaleString() + ' F CFA';
      modal.style.display = 'flex';
    }
  };

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  resForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const guestName = document.getElementById('guestName').value;
    modal.style.display = 'none';
    document.getElementById('successMessage').innerText = `Merci ${guestName}, votre réservation a été enregistrée avec succès. Un SMS de confirmation a été envoyé au numéro indiqué.`;
    successModal.style.display = 'flex';
  });

  // --- TESTIMONIAL SLIDER LOGIC ---
  if (testimonialsTrack) {
    let currentSlide = 0;
    setInterval(() => {
      currentSlide = (currentSlide + 1) % testimonials.length;
      testimonialsTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
      testimonialsTrack.style.transition = 'transform 0.8s cubic-bezier(0.65, 0, 0.35, 1)';
      
      const dots = testimonialsDots.querySelectorAll('.dot');
      dots.forEach((d, i) => {
        d.style.background = (i === currentSlide) ? 'var(--primary)' : '#ddd';
      });
    }, 5000);
  }

  document.getElementById('closeSuccessModal').addEventListener('click', () => {
    successModal.style.display = 'none';
  });
});
