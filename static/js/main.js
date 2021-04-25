let submit=document.getElementById('btn')
let save=document.getElementById('save')

let date = document.getElementById('date');
let klass = document.getElementById('klass');

// let currentDate = document.getElementById('date').value;

// let lessons = document.querySelectorAll('#lasson');
// let hometasks = document.querySelectorAll('#homework');

let request = {
  klass: null,
  date: null
}

let test = {
    "2021-04-16": []
  }

// let toServer = [{
//   date: currentDate,
//   changes: []
// }];

submit.addEventListener('click', (Event) => {
	Event.preventDefault();

	//нажатие на кнопку...
	request.date = date.value;
	request.klass = klass.value;

	fetch('edit-schedule', {
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
	    // data[date.value]
	    // data['2021-06-15']
	    if (Object.keys(data).length != 0) {
		    // console.log('пуст');
		    document.getElementById('tab').innerHTML = null;
	    data[date.value].map((item, index) => (
		  document.getElementById('tab').innerHTML += `<tr><td style="width: 38px;">&nbsp; ${++index}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="${item.lesson}" type="text" class="edittable" alias="${item.lesson}"></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="${item.homework}" type="text" class="edittable" alias="${item.homework}"></td></tr>`
		));
		} else {
			document.getElementById('tab').innerHTML = null;
			document.getElementById('tab').innerHTML += `<tr><td style="width: 38px;">&nbsp; ${1}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${2}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${3}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${4}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${5}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${6}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${7}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${8}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr><tr><td style="width: 38px;">&nbsp; ${9}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="" type="text" class="edittable" alias=""></td></tr>`
			console.log('test');
		}
	  });
});

function check(current, alias) {
    if (current !== alias) {
      save.removeAttribute('disabled');
    } else {
      save.setAttribute('disabled', true);
    }
  }

// save.addEventListener('click', (Event) => {
// 	Event.preventDefault();
// }

function saveChanges(cb){
	var currentDate = document.getElementById('date').value;

	var lessons = document.querySelectorAll('#lasson');
	var hometasks = document.querySelectorAll('#homework');

	var toServer = [{
	  date: currentDate,
	  klass: document.getElementById('klass').value,
	  changes: []
	}];

	Object.values(lessons).map(ls => {
  toServer[0].changes.push({
    lesson: ls.value
  });
});

Object.values(hometasks).map((hw, i) => {
  toServer[0].changes[i].homework = hw.value
});

return cb(toServer)
// console.log(toServer);
}


function sendChanges(){
	saveChanges((changes) => {
		fetch('request-schedule', {
	  headers: {
	    'Content-Type': 'application/json'
	  },
	  method: 'POST',
	  body: JSON.stringify(changes),
	})
	});
}
