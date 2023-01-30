<script>
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	export let task,projects,people;
	const dispatch = createEventDispatcher();
	let editable=false;
        const context_arr=["Email" ,"Errands" ,"Call" ,"Docs" ,"House" ,"Meet" ,"Read" ,"Think" ,"Web" ,"Work"]

	let contexts=[];
        var gtd,difficulty,priority;
        function toggleTaskDetail(){ dispatch('toggle',{text:'toggle'}) }
	onMount(() => {context_arr.forEach(x=>{
		if(task['tags']){
		if(task['tags'].find(y=>x==y)){
			contexts.push(x)
		}
		}
	})});
	function TagStyle(tsk,tg){
		let rv="btn btn-light btn-sm";
			if(tsk['tags']){
				tsk['tags'].forEach((t)=>{if(t==tg){rv="btn btn-dark btn-sm";}});
			}
			return rv;
	}
	function hasTag(tag){
		if(task['tags']){
			return task['tags'].find(t=>t==tag)
		}
		return false;
	}
	function save(){
                let tags=[];
                // task['tags'];
		console.log(contexts);
                if(task['tags']){tags=tags.concat(task['tags']);}
                context_arr.forEach( a=>{
                        let tagMatch=tags.find(x=>x==a);
                        let ctxMatch=contexts.find(x=>x==a);
                        if(ctxMatch && !tagMatch){tags.push(a)}
			if(!ctxMatch && tagMatch){ tags=tags.filter(x=>(x!=a));console.log("post filter",a,tags)}
                });
                task['tags']=tags;
		console.log(task,difficulty,priority)
                editable=false;
		 fetch(
			'/saveTask', {
				method: "POST",
				body: JSON.stringify(task),
				headers: { "content-type": "application/json" }
			})
                        .then(d=>d.text())
			.then(d=>{ console.log(JSON.parse(d))});
	}
</script>


	<slot> 
	<div class="card text-white bg-primary">
	{#if editable}
		<h5 class="card-header">
		<input type="text" bind:value={task['description']} placeholder="Task Title"/>
		<button type="button" class="btn-close float-end" aria-label="Close" on:click={()=>editable=false}> </button> </h5>  
	<div class="row"> 
		<div class="col-2">
			<input type="radio" bind:group={task['tags']} name="Next" value="Next">Next
			<input type="radio" bind:group={task['tags']} name="Waiting" value="Waiting">Waiting
			<input type="radio" bind:group={task['tags']} name="Future" value="Future">Future
		</div>
		<div class="col-2">Project: <select bind:value={task['project']}>{#each projects as p}<option value={p['project']}>{p['project']}</option>{/each} </div>
                <div class="col-2">Assigned: <select bind:value={task['assign']}>{#each people as p}{console.log(p)}<option value={p}>{p}</option>{/each}</select></div>
                <div class="col-2">Difficulty:  <select bind:value={task['difficulty']} ><option value="Low">Low</option><option value="High">High</option></select></div> , 
                <div class="col-2">Priority:  <select bind:value={task['priority']} ><option value="Low">Low</option><option value="High">High</option></select></div> , 
                <div class="col-2">Due </div> <div class="col-2"><input type="datetime-local" bind:value={task['due']}> </div> 
	</div> 
	<div class="row"> 
		<div class="col-12"><strong>Context:</strong>
                <input type="checkbox"  bind:group={contexts} name="context"   value="Email"   > @Email
                <input type="checkbox"  bind:group={contexts} name="context"   value="Errands" > @Errands
                <input type="checkbox"  bind:group={contexts} name="context"   value="Call"    > @Call
                <input type="checkbox"  bind:group={contexts} name="context"   value="Docs"    > @Docs
                <input type="checkbox"  bind:group={contexts} name="context"   value="House"   > @House
                <input type="checkbox"  bind:group={contexts} name="context"   value="Meet"    > @Meet
                <input type="checkbox"  bind:group={contexts} name="context"   value="Read"    > @Read
                <input type="checkbox"  bind:group={contexts} name="context"   value="Think"   > @Think
                <input type="checkbox"  bind:group={contexts} name="context"   value="Web"     > @Web
                <input type="checkbox"  bind:group={contexts} name="context"   value="Work"    > @Work
                </div>
	<div class="row">
		<div class="col-12">Effort:<input type="text" bind:value={task['effort']}></div>
	</div>
	</div>
	<div class="row">
		<div class="col-4"><button class="btn btn-primary" on:click={save}>Save</button></div>
                <div class="col-4"><button class="btn btn-warning" on:click={()=>(editable=false)}>Cancel</button></div>
	</div>

	{:else}
		<div on:dblclick={()=>editable=!editable}>
			<div class="card-header"> <span class="float-center">{task['description']}</span><button type="button" class="btn-close float-end" aria-label="Close" on:click={toggleTaskDetail(task)}> </button> </div>  
	<div class="card-body">
	<div class="row"> 
		<div class="col-3">
			<span class={TagStyle(task,"Next")}>N</span>
			<span class={TagStyle(task,"Waiting")}>W</span>
			<span class={TagStyle(task,"Future")}>F</span>
			<span class={TagStyle(task,"Dismissed")}>X</span>
		</div>  
		<div class="col-9">
			{#if task['project']}Project: <emph class="bg-secondary">{task['project']}</emph>{/if}
			{#if task['assign']}<span >Assigned: <emph>{task['assign']}</emph></span>{/if}
			{#if task['difficulty']}<span >Difficulty: {task['difficulty']}</span> , {/if}
			{#if task['priority']}<span >Priority:  {task['priority']}</span> {/if}
			{#if task['due']}<span >Due </span> <span class="col-2"><emph>{#if task['due']}{task['due'].split('T')[0]}{/if}</emph> </span> {/if}
		</div>
	</div> 
	<div class="row"> 
		<div class="col-1"><strong>Context:</strong></div>
		<div class="col-11" >
			{#each context_arr as ctx}
				{#if (hasTag(ctx))}
					<i> @{ctx} </i> 
				{/if}
			{/each}
		</div>
	<div class="row">
		{#if task['effort']}
		<div class="col-2">Effort: {task['effort']}</div>{/if}
	</div>
	</div>

	<div class="card-text"> 
	{#if task['annotations']}
	Annotation.
	<hr/>
		{#each task['annotations'] as ann}
			<li> <emph> {ann['entry']}</emph> : {ann['description']}</li> 
		{/each}
	{/if}
	</div>
		</div>
		</div>
	{/if}
	</div>
	</slot> 
