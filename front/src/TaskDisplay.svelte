<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	export let task;
	export let showDetail=false;
	let annot=false;
	let hover=false;
	let hoverpersist=false;
	var newAnnotation;

	function redraw() { dispatch('redraw', { text: 'redraw' }); }
	function saveAnnotation(){
		let ann=[]
			if(task['annotations']) {ann.concat(task['annotations'])}
			ann.push({'entry':new Date(),'description':newAnnotation});
		task['annotations']=ann;
		 fetch(
			'/addAnnotate', {
				method: "POST",
				body: JSON.stringify({
					uuid: task['uuid'],
					annotation: newAnnotation
				}),
				headers: { "content-type": "application/json" }
			});
	}
	function markDone(tsk){
		 fetch(
			'/done', {
				method: "POST",
				body: JSON.stringify({
					id: task['id'],
					uuid: task['uuid']
				}),
				headers: {
					"content-type": "application/json"
				}
			});
	}
	function toggleSubtask(){
	}
</script>
<slot name="task"><li> <input type="checkbox" on:click={()=>{markDone(task)}} >
	<span on:click={()=>(showDetail=!showDetail)}> {task['description']} {#if task['assign']}[ {task['assign']} ]{/if}</span>
		<i class="fa-solid fa-pen-fancy text-primary" on:click|stopPropagation={()=>{annot=!annot}}></i>
		{#if task['depends']} <span class="badge bg-secondary" on:click|stopPropagation={()=> {
		task['showSubtasks']=!task['showSubtasks'];
		redraw(); }}>+</span> {/if}
	{#if task['annotations']}
			<i on:click|stopPropagation={()=>hoverpersist=!hoverpersist} on:mouseover={()=>hover=true} on:mouseleave={()=>hover=false} class="fa-regular fa-clipboard text-primary"></i>
				{#if hoverpersist||hover}
					<div style="position:relative;margin-right=-100px;background-color:#aaaaaa; opacity:50">
						{#each task['annotations'] as ann}
							<div class="row"><div class="col-4">{ann['entry']}</div><div class="col-8"> {ann['description']}</div></div>
						{/each}
					</div>
				{/if}

	{/if}
			{#if annot} <div > <textarea bind:value={newAnnotation}></textarea> <button class="btn btn-primary"  on:click|stopPropagation={saveAnnotation}>Save</button> </div>{/if}
	</li>
</slot>
