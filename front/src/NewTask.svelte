<script>
	let toggleDisplay=false;
	let task={};
	function save(){
		console.log(task)
		 fetch(
			'/newTask', {
				method: "POST",
				body: JSON.stringify(task),
				headers: { "content-type": "application/json" }
			})
				.then(d=>console.log(d));
	}
</script>
<slot>
<button type="button" class="btn btn-primary btn-sm" on:click={()=>{console.log(toggleDisplay);toggleDisplay=!toggleDisplay}}>New Task</button>
	{#if toggleDisplay}
<span>
			<div class="form-group row">
				<label for="description" class="col-sm-2 form-control-label">Task</label>
				<div class="col-sm-10">
					<input type="text" class="form-control" id="description"   bind:value={task['description']} placeholder="This needs to be done"/>
				</div>
			</div>
			<div class="form-group row">
				<label for="project" class="col-sm-2 form-control-label">Project</label>
				<div class="col-sm-10">
					<input type="text" class="form-control" id="project"  bind:value={task['project']} placeholder="What project is this a part of"/>
				</div>
			<div class="form-group row">
				<label for="assign" class="col-sm-2 form-control-label">Assigned to</label>
				<div class="col-sm-10">
					<input type="text" class="form-control" id="assign"  bind:value={task['assign']} placeholder="Who will do this"/>
				</div>
			</div>
			<div class="form-group row">
				<label for="due" class="col-sm-2 form-control-label">By When should it be done?</label>
				<div class="col-sm-10">
					<input type="date" class="form-control" id="due" bind:value={task['due']}/>
				</div>
			</div>
			<div class="form-group row">
				<div class="col-sm-offset-2 col-sm-10">
					<button type="submit" class="btn btn-secondary btn-sm" on:click={save}>Add Task</button>
				</div>
			</div>
	</span>
	{/if}
</slot>
