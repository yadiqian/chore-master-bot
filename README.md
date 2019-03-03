# chore-master-bot

A GroupMe bot that schedules weekly chores for all members in the group. Useful for a roommate GroupMe chat.  

## Commands

Here are all the currently supported commands.

### /add

To add a chore. It takes the name of the chore and the number of people needed for the chore as arguments.

```
/add <chore name> <number of helpers>
```

```
/add putting away the dishes 2
```

```
/add sweeping the floor 1
```

### /delete

To delete an existing chore. It takes the ID of the chore as argument. To see the ID of all chores, use the command /show chore list.


```
/delete <chore ID>
```

```
/delete 3
```

### /reset

To change the number of helpers for a chore. It takes the ID of a chore and the new number of helpers as arguments. To see the ID of all chores, use the command /show chore list.

```
/reset <chore ID> <new chore ID>
```

```
/reset putting away the dishes 1
```

### /show chore list




CREATE TABLE chores (
	id serial PRIMARY KEY,
	name text NOT NULL,
	num_helper INT NOT NULL
);

CREATE TABLE chore_assignment (
	name text NOT NULL,
	chore text NOT NULL	
);