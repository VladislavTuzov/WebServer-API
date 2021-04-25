let submit=document.getElementById('btn')

let date = document.getElementById('date');
let klass = document.getElementById('klass');

let request = {
  klass: null,
  date: null
}

submit.addEventListener('click', (Event) => {
	Event.preventDefault();

	//нажатие на кнопку...
	request.date = date.value;
	request.klass = klass.value;

	fetch('schedule', {
	  headers: {
	    'Content-Type': 'application/json'
	  },

	  method: 'POST',
	  body: JSON.stringify(request),
	})
	  .then((data) => {
	    return data.json();
	  })

	  .then((data) => {
	    console.log(data[date.value]);
	    data[date.value].map((item, index) => (
	    	console.log(item.lesson)
			document.getElementById('tab').innerHTML += `<tr><td style="width: 38px;">&nbsp; ${++index}</td><td style="width: 151px;">${item.lesson}</td><td style="width: 390px;">${item.homework}</td></tr>`
		));
	  });
	// alert(date.value, klass.value);
	// console.log(klass.value);
});
