// BEGIN - effect functions

// Runs a blind effect to toggle on a form and toggle off the show form button
var blindEffect = function(model, id) {
  $('#' + model + '-button' + id).toggle('blind', {}, 2000);
  $('#' + model + '-form' + id).toggle('blind', {}, 2000); 
};

// END - effect functions
