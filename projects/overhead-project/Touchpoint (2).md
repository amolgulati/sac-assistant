# Touchpoint

Source: `Touchpoint (2).docx`

Date: April 1, 2026, 3:04 PM

## Transcript

Touchpoint-20260401_100428-Meeting Recording

Gulati, Amol started transcription

Roundtree, Jayce C 0:03 So where you're going to start is underneath this modeler button and once you click on that you get the option to create a new model or you can go to the dimension tables. So these are the public ones that whether it's Applexus or myself has created.

Gulati, Amol 0:09 Yeah. Yeah.

Roundtree, Jayce C 0:22 And you can kind of do a sort to see the ones that are tied into the stuff that we're getting in as in Datasphere. So there's this profit center and a reporting account and a cost center.

Gulati, Amol 0:32 OK.

Roundtree, Jayce C 0:39 So these will have all the hierarchy items. So if we click on the reporting account, this is coming out and getting all of our stuff and then it's giving it the parent child hierarchy that it needs to build these relationships.

Gulati, Amol 0:57 OK.

Roundtree, Jayce C 1:03 You see it's using this OData service. So I have a view set up that'll go out and it's updating this dimension on a daily basis. So this is something you won't have to maintain manually. I think the same thing with the profit center. All three of these that'll be utilized, it's all set up against what we have in Datasphere. It has the parent child. This one isn't scheduled, but we could set it on a schedule. It's coming from a view in Datasphere. As you're creating models, you don't have to create the dimension every time.

Gulati, Amol 2:12 OK. Yeah, OK.

Roundtree, Jayce C 2:23 So that's available out there. So that should help a bunch. What we can start with is the salary planning model. This will be just supportive models that we're using to push data from how the end user wants to load the information, and then we push it to the final model that they'll use for budgeting. When you create it, it's auto going to create a version dimension.

Gulati, Amol 4:31 OK, so wait, how did you just get all of this data in this nice format by month?

Roundtree, Jayce C 4:54 No, this is prebuilt SAP stuff. They create this date dimension and that's standard across the board.

Gulati, Amol 5:14 Uh, OK, it has to be fixed. It can't be like a dynamic time range.

Roundtree, Jayce C 5:52 Yeah, I would say eventually it probably should be dynamic. I would do some research and we'll see if there's a data action that can be created to change this.

Gulati, Amol 6:17 OK, yeah, OK.

Roundtree, Jayce C 6:26 On the version it's always going to default to actual, but this is where you can set up budget and other scenarios. Then you can see it's going to say there's no element created for the measures, so you need to do that so it has a place to store the value.

Roundtree, Jayce C 7:28 The aggregation we're going to want at first is sum and then we can use calculations if we need to tell it to do differently.

Gulati, Amol 7:31 Yeah. OK, I guess I thought in my mind that you don't have to create these dimensions manually, but I guess you're creating a brand new model.

Roundtree, Jayce C 7:53 It's just like this is the first time setup.

Roundtree, Jayce C 8:13 Then you add an existing dimension table and pick the spend profit center, reporting account, cost center, and anything else users need to enter data against.

Gulati, Amol 9:01 OK. So there's a separate dimension for SG&A cost center.

Roundtree, Jayce C 9:11 I think when I created it, I didn't have any other needs for the cost center, so I was just giving them a name. I mostly brought in the executive and functional views rather than the full work-sequence hierarchy.

Roundtree, Jayce C 10:37 This is where you can create the ways that people will load the information. I can go to a preview-built model and look at that data management.

Gulati, Amol 11:04 OK, so when you create this model, it's blank by default. It doesn't automatically load in anything.

Roundtree, Jayce C 11:10 Correct. They have a job set to where it can read a CSV file. We could give them one location to put the data and then have a data action that comes out and runs this job.

Roundtree, Jayce C 12:06 It reads the file and then maps it to profit center, cost center, date, and other dimensions. Then if no issues are found you hit finish and import it into the model.

Roundtree, Jayce C 14:04 At that level I had stuff loaded to the merit increase column and we have a place where we could do the burden as well, but then the salaries were loaded.

Gulati, Amol 14:12 OK, I see. So this is like the true SAC planning model that lives purely in SAC and has got the data actions, you're doing the calculations and then you would send it to another model after that.

Roundtree, Jayce C 14:47 It's still SAC. This is basically just a supporting model that's gonna allow input of data and then we can control how it's gonna get pushed over to the final one where people are making changes and reviewing their budget.

Roundtree, Jayce C 15:21 One thing I'll show you is the merit increase. For the user, they're only inputting what they want the merit increase to be by date. That will then apply to everything since we don't have a specific profit center or cost center. That's where the calculations come in.

Roundtree, Jayce C 17:46 This is where we loaded it to the merit increase measure. The calculation is the merit calc. This is where it's going out and pushing that to all the profit centers for all the months so we don't have to do it over and over.

Gulati, Amol 17:52 Yeah, so merit increase is just a percent and the calc is taking that merit increase times whatever dimension we pick, right?

Roundtree, Jayce C 18:13 Yeah. It spreads on the profit center. First three months, no increase. Everything else you got a 4% increase. Then if you add the cost center too, that same percentage is being applied to every cost center on that process.

Gulati, Amol 18:58 And then you chose the first three months no increase and then the rest of the months 4% increase. You put that in there.

Roundtree, Jayce C 19:08 Yeah, that was part of the data load from the CSV file for test purposes.

Roundtree, Jayce C 19:39 What this does is it allows us to use the data action to load the merit calc and not the raw merit increase measure to the final model.

Gulati, Amol 20:16 And this is just for salaries.

Roundtree, Jayce C 20:19 Yeah, this one model is where we're handling all of the data setup and manipulation for salaries before it goes to the final planning model.

Roundtree, Jayce C 20:47 When you do the mapping you can say I want it to go to employee wages. It auto generates rules for every profit center in the source. The same thing would be for cost center, date, and things like that.

Roundtree, Jayce C 22:26 The warning is basically saying in your file right now you only have 433 distinct cost centers, but there are many more available in the cost center dimension. As long as you have the triangle, you're good. If you have an X, that's a different story.

Roundtree, Jayce C 23:26 You could have one data action that writes salaries, one that writes merit, and one that writes burden. Or you could combine them. You create dynamic functionality using parameters so the user is prompted for what budget scenario they want to run it for.

Roundtree, Jayce C 25:24 That's how you push data from the salary planning model into the final SG&A and OE planning model where you would have your actuals, budget, and whatever the case may be.

Roundtree, Jayce C 27:01 When I created the account dimension I created some manual placeholders like bonus rate, burden rate, merit increase. Bottom line is they would have a place where those values populate and then they can adjust if needed. Then you would have a calculation that says take salary times merit increase and it would have a dynamic calculation within the model.

Gulati, Amol 29:25 OK, so whatever supporting model we use for salaries, you're now applying that same logic to a different reporting account, like burden.

Roundtree, Jayce C 30:30 The default in the model is to aggregate using sum. So for merit increase we don't want Q1 to become 3 just because it is one plus one plus one. We want it to be average, so I created another line and said set it equal to the merit increase and use exception aggregation so null or zero values are ignored.

Roundtree, Jayce C 31:50 We may want to create another standalone account called baseline salary and load to that. Then users could adjust on the wages line, while the baseline remains locked.

Roundtree, Jayce C 33:09 For burden and merit increase, we can then do that on a separate account as well or at the aggregated node, but that's step two. First is getting the planning model built and then loading data and getting it to push to the final model.

Gulati, Amol 34:29 What you just did for salaries, does that apply to all of the salary accounts or is that just one particular GL account?

Roundtree, Jayce C 34:49 What I would do is just map it to one wages member for now. That way it just rolls into the employee wages line and aggregates up correctly.

Roundtree, Jayce C 36:35 We just need to create the planning model and create the data action to load the information.

Gulati, Amol 37:05 Then there'd be one separate one for burden, right?

Roundtree, Jayce C 37:09 The burden could be included in this, but we'd need to load it at the level of detail you want.

Gulati, Amol 38:18 I guess next three.

Roundtree, Jayce C 38:20 I would say you'd have salary planning, which would include salary baseline, merit increase, and burden, and then another for non-employee expenses where we try to capture the trailing 12-month average and spread it across the next year.

Gulati, Amol 39:00 Burden benefits, I guess. OK. This helps a lot. I'm going to try and recreate this.

Roundtree, Jayce C 39:16 Yeah, that would be the good first step: get the model created, load salaries, load merit, create the calculation, and then create a data action to move it to the final model.

Gulati, Amol 40:41 One thing I wanted to show you was something on Databricks. Jennifer sent me this extremely ugly management report. I was playing around in Databricks and I created tables from the first five tabs and built an agent over it. It's pretty cool because it lets you chat with the data and pull up graphs.

Gulati, Amol 43:41 I want your thoughts on maybe who to show this to. Databricks isn't in production yet, so I don't want to get ahead of my skis, but I will have to present to the Steerco later this April and I need some way of showing what Databricks can do.

Roundtree, Jayce C 43:52 I think that would be more of a Jennifer question. I think that's part of what they're looking for: the ability to ask common language questions and get some sort of analysis.

Roundtree, Jayce C 44:58 I think it's worth mentioning it to her and saying if we can get the data loaded or have a model that holds all the information for the management report, then they can ask it questions.

Gulati, Amol 45:22 This is all consolidated last numbers that people see, and if this could be tabular and searchable historically, I would think it would be valuable.

Roundtree, Jayce C 46:40 I would just take a brief meeting with Jennifer and say this is something you loaded manually, these are the kinds of things we can do in Databricks, and ask whether there's any interest.

Roundtree, Jayce C 47:13 It would also be interesting to ask what type of questions they would want to ask in common language and get answers from.

Roundtree, Jayce C 48:21 One thing to test out would be cost per BOE, what's driving it, what's causing it to go up or down, and what business units are driving that.

Gulati, Amol 49:16 My vision would be if they are interested in something like this, they'd need to log this and save it historically for the last 12 to 24 months, compare across periods, and potentially tie tabs back to each other.

Roundtree, Jayce C 50:20 Yeah, and I could see us getting there.

Gulati, Amol 50:38 I'll let you know.

Roundtree, Jayce C 50:53 OK, sounds good.

Gulati, Amol 50:55 All right. Thanks, Jason.

Roundtree, Jayce C 51:00 Alright, bye.

Gulati, Amol stopped transcription
