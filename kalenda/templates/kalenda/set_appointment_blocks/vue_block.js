// TODO Transfer this js file to static after done. Lets keep the templates folder with pure HTML files only

var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
    select_time: true,
    select_length: false,
    enter_details: false,
    review: false,
    confirmed: false
  },
  methods: {
    reset: function(){
        this.select_time = false;
        this.select_length = false;
        this.enter_details = false;
        this.review = false;
        this.confirmed = false;
    },
    view_block: function (block_name) {
      this.reset()
      this[block_name] = true
    }
  }
})
