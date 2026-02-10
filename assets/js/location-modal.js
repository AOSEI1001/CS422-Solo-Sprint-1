(function(){
  const locations = [
    'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Phoenix, AZ',
    'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA', 'Dallas, TX', 'San Jose, CA',
    'Austin, TX', 'Jacksonville, FL', 'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC',
    'San Francisco, CA', 'Boston, MA', 'Seattle, WA', 'Denver, CO', 'Miami, FL'
  ];

  const searchInput = document.getElementById('locationSearchInput');
  const optionsContainer = document.getElementById('locationOptions');
  const confirmBtn = document.getElementById('confirmLocation');
  const cityInput = document.getElementById('city');
  let selectedLocation = '';

  function renderOptions(query) {
    let filtered = locations;
    if (query) {
      filtered = locations.filter(loc => 
        loc.toLowerCase().includes(query.toLowerCase())
      );
    }
    
    optionsContainer.innerHTML = filtered.slice(0, 10).map(loc => `
      <a href="#" class="list-group-item list-group-item-action location-option" data-location="${loc}">
        <i class="fa fa-map-marker"></i> ${loc}
      </a>
    `).join('');

    // Add click listeners to options
    document.querySelectorAll('.location-option').forEach(option => {
      option.addEventListener('click', (e) => {
        e.preventDefault();
        selectedLocation = option.dataset.location;
        document.querySelectorAll('.location-option').forEach(o => 
          o.classList.remove('active')
        );
        option.classList.add('active');
      });
    });
  }

  searchInput.addEventListener('input', (e) => {
    renderOptions(e.target.value);
  });

  confirmBtn.addEventListener('click', () => {
    if (selectedLocation) {
      cityInput.value = selectedLocation;
    }
  });

  // Initialize on modal show
  const modal = document.getElementById('locationModal');
  modal.addEventListener('show.bs.modal', () => {
    searchInput.value = '';
    selectedLocation = '';
    renderOptions('');
    searchInput.focus();
  });
})();
