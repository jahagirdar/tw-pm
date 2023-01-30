<script>
	import { onMount } from 'svelte';
	import TaskDisplay from './TaskDisplay.svelte';
	import TaskDetail from './TaskDetail.svelte';
	import NewTask from './NewTask.svelte';
	let me="Vijayvithal";
	let show_menu=false;

        let tasks = {'pending':[ ] };
        let projects=[];
        let dirtyTask=[];
	let detailTasks=[];
	let selectedProjects=[];
        let detailsChanged=0;

        let nextTasks=[];
        let futureTasks=[];
        let waitingTasks=[];
        let inboxTasks=[];
	let subProjects=[];
        let people=[];
        var newPerson;
        let show_person_form=false;

	onMount(() => {
		getTasks();
		getProjects();
	});
	function forceRedraw(){
		//console.log("force redraw");
		tasks=tasks;
	}

        function addPerson(){
                if (!people.includes(newPerson)){
                people.push(newPerson);
                }
                show_person_form=false;
        }
        function sortTasks(){
		var task;
		console.log("Do Sort");

		inboxTasks=[];
		waitingTasks=[];
		futureTasks=[];
		nextTasks=[];
		subProjects=[];
		tasks['pending'].forEach((task)=>{
			if(selectedProjects.includes(task['project'])||(selectedProjects.includes(null) && !task['project'])){
				if(task['depends'] && (hasActiveChild(task))){
					task['showSubtasks']=false;
					subProjects.push(task);
				}else if(task['start']){
					task['show']=true;
					nextTasks.push(task);

				}else if(task['assign']!=me && task['assign']){
					waitingTasks.push(task);
				}else if(task['tags']){
				if(task['tags'].includes("Next")){
					task['show']=true;
					nextTasks.push(task);
				}else if(task['tags'].includes("Future")){
					futureTasks.push(task);
				}else if (task['tags'].includes("Waiting")){
					waitingTasks.push(task);
				}
				else {
					inboxTasks.push(task);
				}
				}
				else {
					inboxTasks.push(task);
				}
			}
		});
		inboxTasks=inboxTasks;
		waitingTasks=waitingTasks;
		futureTasks=futureTasks;
		nextTasks=nextTasks;
			// console.log(selectedProjects,"inbox ",inboxTasks,"future=",futureTasks,"Next",nextTasks,"subprojects",subProjects,"assign",waitingTasks);
	}
	function hasActiveChild(tsk){
		let rv=false;
		if(tsk['depends']){
			rv=tsk['depends'].find((uuid)=>{
				return tasks['pending'].find((task)=> {
					// console.log( task['uuid'],uuid,task['uuid']==uuid);
					return task['uuid']==uuid;
				}
				)
			})
			if(rv){console.log("rv is true");}
		}
		return rv
	}

        function saveTask(task){
                if (!dirtyTask.includes(task['uuid'])){
                        dirtyTask.push(task['uuid']);
                }
                dirtyTask=dirtyTask;
        }
        function hasTag(tsk,tg){
                let rv=false;
                if(tsk['tags']){
                        tsk['tags'].forEach((t)=>{if(t==tg){rv='true';}});
                }
                return rv;
        }
        function TagStyle(tsk,tg){
                let rv="btn btn-light";
                        if(tsk['tags']){
                                tsk['tags'].forEach((t)=>{if(t==tg){rv="btn btn-dark";}});
                        }
                        return rv;
        }
        function setEditable(tsk){
                tsk['editable']=true;
                tasks=tasks;
        }
        function toggleTaskDetail(tsk){
                detailsChanged +=1
                tsk['editable']=false;
                if (detailTasks.includes(tsk['uuid'])){
                        detailTasks=detailTasks.filter((x)=>(x!=tsk['uuid']));
                }
                else {
                        detailTasks.push(tsk['uuid']);
                        detailTasks=detailTasks;
                }
        }
        function getTasks() {
                fetch('/tasks')
                        .then(d=>d.text())
			.then(d=>{
				tasks=JSON.parse(d);
				processTasks();
				findPeople();
			});
        }
	function toDate(dt){
		return new Date(dt.replace(/(....)(..)(..)T(..)(..)(..)Z/,"$1-$2-$3T$4:$5:$6Z"));
	}
	function toDateStr(dt){
		return dt.replace(/(....)(..)(..)T(..)(..)(..)Z/,"$1-$2-$3T$4:$5");
	}
	function processTasks(){
		tasks['pending'].forEach(tsk=>{
			if(tsk['due']){
				tsk['due']=toDateStr(tsk['due']);
			}
			if(tsk['entry']){
				tsk['entry']=toDate(tsk['entry']);
			}
			if(tsk['modified']){
				tsk['modified']=toDate(tsk['modified']);
			}
			if (tsk['annotations']){
				tsk['annotations'].forEach( a => {a['entry']=toDate(a['entry'])});
			}


		});
	}
	function findPeople(){
		tasks['pending'].forEach((task)=>{
			if(task['assign']){
				if (!people.includes(task['assign'])){
					people.push(task['assign']);
				}
			}
		});
		people=people;
	}
        function getProjects() {
                fetch('/projects')
                        .then(d=>d.text())
                        .then(d=>{
                                projects=JSON.parse(d);
                                });
        }
        function toggleProject(prj){
                projects[prj.id]['selected']=!prj['selected'];
                updateSelected();
		sortTasks();
		tasks=tasks;
        }
        function updateSelected(){
                selectedProjects=[]
                        projects.forEach( (p)=>{
                                if (p['selected']){
                                        selectedProjects.push(p['project']);
                                }});
        }

        function getStyle(prj){
                if(prj['selected']) return "btn btn-dark btn-sm";
		else return "btn btn-light btn-sm";
        } 
</script>

<div class="container">
	<span class="fa-solid fa-bars" on:click={()=> show_menu=!show_menu}></span>

		{#if show_menu}
<button class="btn btn-primary btn-sm" on:click={getProjects}>Load Projects</button>
<button class="btn btn-primary btn-sm" on:click={getTasks}>Load Tasks</button>
<button class="btn btn-primary btn-sm" on:click={()=>(show_person_form=true)}>Add Person</button>
<NewTask/>
		{/if}

{#if show_person_form}
        <input type=text bind:value={newPerson}>
        <button class="btn btn-primary btn-sm" on:click={addPerson}>Save</button>
{/if}
<h1> Projects</h1>

{people}
<div class="row"><div class="col-12">
                {#each projects as project}
                        <button type="button"
                                class={getStyle(project)}
				on:click={()=>{toggleProject(project)}}>{project['project']}</button> 
                {/each}
        </div>

</div>
<h1> Tasks</h1>
<ul>
                <div class="row">
                        <div class="col-4">
                                <h2>Unprocessed Inbox</h2>
				{#each inboxTasks as task}
                                        {#if task['show']}
						<div  on:click={toggleTaskDetail(task)} > <TaskDisplay task={task}/> </div>
                                        {/if}
                                {/each}
                        </div>
                        <div class="col-4">
                                <h2>Next Tasks</h2>
				{#each nextTasks as task}

                                        {#if task['show']}
						<div  on:click={toggleTaskDetail(task)} > <TaskDisplay task={task}/> </div>
                                        {/if}
                                {/each}
                                <h2>Subprojects</h2>
				{#each subProjects as task}

                                        {#if task['show']}
						<div  on:click={toggleTaskDetail(task)} > <TaskDisplay task={task} on:redraw={forceRedraw}/> </div>
                                        {/if}
                                {/each}
                        </div>
                        <div class="col-4">
                                <h2> Assigned Tasks</h2>
				{#each waitingTasks as task}

                                        {#if task['show']}
						<div  on:click={toggleTaskDetail(task)} > <TaskDisplay task={task} on:redraw={forceRedraw}/> </div>
                                        {/if}
                                {/each}
                                <h2> Future Tasks</h2>
				{#each futureTasks as task}

                                        {#if task['show']}
						<div  on:click={toggleTaskDetail(task)} > <TaskDisplay task={task}/> </div>
                                        {/if}
                                {/each}
                        </div>
                </div>
</ul>
<div>
        {#each tasks['pending'] as task}
                {#if detailTasks.includes(task['uuid'])}
                        <div class="card light-gray" >
				<TaskDetail on:toggle={()=>toggleTaskDetail(task)} task={task} projects={projects} people={people}/>
                        </div>
                {/if}
        {/each}
        {#each tasks['pending'] as task}
		{#if task['showSubtasks']}
			<h3>{task['description']}</h3>
			{#each task['depends'] as dep}
				{#each tasks['pending'] as subtask}
					{#if subtask['uuid'] == dep}
						<TaskDisplay task={subtask} on:redraw={forceRedraw}/>
						<div on:click={()=>{console.log(subtask)}}> show task log</div>
					{/if}
				{/each}
			{/each}
		{/if}
	{/each}
</div>
</div>
