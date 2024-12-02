function getCSRFToken() {
    return window.csrfToken; 
  }

const form = document.getElementById('add-reward');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);
        console.log(formData);
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData, 
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (!response.ok) {
              const result = await response.json();
              
              Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: Object.values(result).flat().join(', ') || 'A problem had appear',
                  confirmButtonColor: 'var(--primary-100)',
                  color: 'var(--text-100)',
                  background: 'var(--bg-100)',
              });
              return;
          }

            const result = await response.json();
            
            
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'New reward created.',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            }).then(() => {
                location.reload();
            });

        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message || 'A problem had appear',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            });
        }
      });
      

      async function deleteReward(reward_id) {
        const result = await Swal.fire({
            title: `Deleting the reward`,
            text: "This action cant be undone",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Delete',
            cancelButtonText: 'Cancel',
            reverseButtons: true,
            confirmButtonColor: 'var(--primary-100)', 
            cancelButtonColor: 'var(--primary-300)', 
            color: 'var(--text-100)', 
            background: 'var(--bg-100)' 
        });

    
        if (result.isConfirmed) {
            try {
                const response = await fetch(`/administration/rewards-api/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken() 
                    },
                    body: JSON.stringify({reward_id}) 
                });
        
                
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Reward deleted.',
                    confirmButtonColor: 'var(--primary-100)',
                    color: 'var(--text-100)',
                    background: 'var(--bg-100)',
                }).then(() => {
                    window.location.reload(); 
                });
            } else {
                const errorData = await response.json();
                Swal.fire({
                    icon: 'error',
                    title: 'Error!',
                    text: `Error: ${errorData.detail || 'Error, not deleted.'}`,
                    confirmButtonColor: 'var(--primary-100)',
                    color: 'var(--text-100)',
                    background: 'var(--bg-100)',
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error!',
                text: 'An error occurred: ' + error.message,
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            });
        }
    }
}