// Store selected location
let selectedLocation = null;

let weatherId = document.getElementById('weather-data');




// Initialize location search on page load
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('locationSearchInput');
  const locationOptions = document.getElementById('locationOptions');
  const confirmBtn = document.getElementById('confirmLocation');

  // Live search as user types
  searchInput.addEventListener('input', async function() {
    const searchTerm = this.value.trim();
    
    if (searchTerm.length < 2) {
      locationOptions.innerHTML = '';
      return;
    }

    try {
      // Using Google Places API Autocomplete service
      if (!window.google || !window.google.maps || !window.google.maps.places) {
        locationOptions.innerHTML = '<div class="list-group-item text-danger">Google Maps API not loaded</div>';
        return;
      }

      const autocompleteService = new google.maps.places.AutocompleteService();
      
      autocompleteService.getPlacePredictions(
        {
          input: searchTerm
        },
        (predictions, status) => {
          locationOptions.innerHTML = '';

          if (status !== google.maps.places.PlacesServiceStatus.OK && status !== google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
            console.error('Autocomplete status:', status);
            locationOptions.innerHTML = '<div class="list-group-item text-muted">No locations found</div>';
            return;
          }

          if (!predictions || predictions.length === 0) {
            locationOptions.innerHTML = '<div class="list-group-item text-muted">No results</div>';
            return;
          }

          predictions.forEach(prediction => {
            const locationDisplay = prediction.description;
            
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'list-group-item list-group-item-action';
            button.style.padding = '12px 15px';
            button.style.cursor = 'pointer';
            button.innerHTML = `<strong style="color: #333; font-size: 14px; display: block;">${locationDisplay}</strong>`;
            
            button.addEventListener('click', function(e) {
              e.preventDefault();
              selectedLocation = locationDisplay;
              
              // Highlight selected item
              document.querySelectorAll('#locationOptions .list-group-item').forEach(item => {
                item.classList.remove('active');
              });
              this.classList.add('active');
              
              // Auto-submit form after selection
              submitWeatherSearch(selectedLocation);
            });
            
            locationOptions.appendChild(button);
          });
        }
      );
    } catch (error) {
      console.error('Error fetching locations:', error);
      locationOptions.innerHTML = '<div class="list-group-item text-danger">Error loading locations</div>';
    }
  });

  // Confirm button action
  confirmBtn.addEventListener('click', function() {
    if (selectedLocation) {
      submitWeatherSearch(selectedLocation);
    }
  });
});

// Helper function to submit weather search form
function submitWeatherSearch(location) {
  // Create and submit form with the selected location
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/';
  
  const input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'city';
  input.value = location;
  
  form.appendChild(input);
  document.body.appendChild(form);
  form.submit();
}

function updateLocalTime() {
  if (weatherId) {
    // Get UTC time and adjust by timezone offset
    let weatherData = JSON.parse(weatherId.textContent);
    
    if(weatherData && weatherData.timezone){
      const now = new Date();
      const utcTime = now.getTime() + now.getTimezoneOffset() * 60000;
      const localTime = new Date(utcTime + (weatherData.timezone * 1000));
      
      document.getElementById('localTime').textContent = localTime.toLocaleTimeString();
    }

    


    
  }
}

// Update time every second
setInterval(updateLocalTime, 1000);
updateLocalTime(); // Initial call