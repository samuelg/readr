// BEGIN - effect functions

// Runs a blind effect to toggle on a reading form and toggle off the read this button
var readBlindEffect = function(id) {
  $('#reading-button' + id).toggle('blind', {}, 2000);
  $('#reading-form' + id).toggle('blind', {}, 2000); 
};

// END - effect functions
