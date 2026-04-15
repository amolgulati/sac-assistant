# Touchpoint 3.11.26

Source: `Touchpoint 3.11.26.docx`

Date: March 11, 2026, 3:09 PM

## Transcript

Transcript

Amol 0:03 Alright, so if I want to create a story. Responsive or canvas. Or is there any easier way to do this?

Jayce C 0:25 No, that's the way to do it. Responsive will change size based on the screen. The canvas will stay fixed. In this situation you would just pick responsive.

Jayce C 1:01 Then you'll go underneath tools.

Amol 1:07 Add new data, then I'm going to select that planning model, right?

Jayce C 1:11 Yeah, so I'm gonna click the cube.

Amol 1:16 And then that's SG&A OE planning. Yeah, this one.

Jayce C 1:28 From there you can just add a table.

Amol 1:35 Yeah. And let's say one. I see. OK, so you add them one by one if you want to add a table.

Jayce C 2:14 Yeah.

Amol 2:31 It's just not at all for now. What in rate calc? Why did that come in?

Jayce C 2:44 I think that's a calculation.

Amol 2:48 Yeah. OK, alright, so now basically I have this data. What I'm next step would be kind of create a story that makes sense for the corporate team first and the users. Whoever our target group is.

Jayce C 3:55 I think for the budget you have to pick the forecast layout on the table type.

Amol 4:13 OK, how do I do that?

Jayce C 4:16 On the right-hand side panel.

Amol 4:17 Yes. OK, forecast layout.

Jayce C 4:40 From there it says you can look back, look ahead, and what's your cut-over date. So you can pick that you want to see actuals and the budget.

Amol 4:54 Yes. Cut-over date probably today, right? Or last booked actuals.

Jayce C 5:04 Yeah. This is where we just have to mess around with it and see what works.

Amol 5:57 Maybe because the budget doesn't go for 12 months.

Jayce C 5:58 Yeah, I may not have all the months in there, so just pick the last booked actuals.

Amol 6:52 Oh, I see. So you have to load it because it's not an automated updated model right now.

Jayce C 7:07 Yeah, right now.

Amol 7:08 OK, that can all be changed later. In terms of planning stuff, people can actually input numbers already.

Jayce C 7:45 The stuff that has the hollow bar at the top is input-capable.

Amol 7:59 These are actuals, so that makes sense. And yeah, I can put in a number there. So the calculations are happening on the model itself, right?

Jayce C 8:49 Yeah, if there's a calculation in there, it will be.

Amol 9:04 Seems like there is a calculation because I put 30 here and it auto-filled down.

Jayce C 9:09 That's the default from SAC where if you input it at an aggregate level then it's going to allocate it down underneath it.

Amol 10:11 So what do you think would be the next step. Just try and put together the story and maybe another page with visuals? Or are there actual calculations I need to get programmed into the model?

Jayce C 10:53 First step would just be getting a story created that allows them to put their data. Then once we have a story and it's working like they want to, we can create a feature that's gonna load salaries based on a certain thing and auto-calculate burdens.

Amol 11:48 So first step is just get the story to look somewhat decent that they want to have and then go into the actual data model and put in the logic.

Jayce C 12:20 Yeah.

Amol 12:20 I don't think they care about visuals and charts right now. I think they just want a flat Excel-like file and to be able to see the calculations on what it's doing.

Jayce C 13:32 Put in filters like profit center and cost center.

Amol 14:06 Yeah, I see. Try to pin it to the top.

Jayce C 15:00 At the bottom there is an option that says pin it.

Amol 15:24 I think at this point step one I'll try and get the story to look decent and maybe work with them directly to figure out what they want to see. Step two then go to the data model and start putting in the calculations.

Jayce C 16:15 You can do stuff like auto-populate the salary. I think that SG&A salary planning is where I was attempting that.

Amol 17:07 Over here on the left.

Jayce C 17:08 Yeah, do like a data action and multi-actions.

Amol 18:02 So maybe you have to create a data action first.

Jayce C 18:41 I'll have to remember how to do this again.

Amol 19:48 If I have the goal in mind, I'll look up how to do that using these screens.

Jayce C 20:19 What I did is I had a source model, like salary planning, and a target model, which would be the one you're working on. Then you can put a filter in there for what version you want to source from and other filters like 2025 salaries and one account. Then you can map it and even say take October 2025 and push it to all the months in 2026.

Jayce C 21:52 Then when you're ready, that becomes an action and you can insert a data action starter or multi-action starter button on the story. When they press the button it's going to run that action. This is where I was copying salaries to the model.

Amol 23:08 Well, how would they input the 3% or is that already baked into your action?

Jayce C 23:14 That's where the setup in the model comes into play because you could see this is a measure. In this model I had a burden increase and a merit increase as separate measures, and that's where they were loading values.

Jayce C 23:57 Then it would take the salary times whatever percentage is up there. Same thing with the burden as it would take salary and multiply by the burden rate.

Amol 24:29 So to create that action initially, did you go to data action or multi-step?

Jayce C 24:42 I'm trying to figure out because I don't remember.

Amol 24:52 Data actions. Yeah, they had a data action here.

Jayce C 26:30 That's maybe where you have to watch some videos, and if you find out we don't have access, then we may have to ask why.

Amol 26:41 Yeah, it seems like they removed it.

Jayce C 26:43 Maybe they took it away accidentally.

Amol 26:47 Yeah, it's almost like it used to be there for you, but now it's not there for us.

Jayce C 27:19 It doesn't look like we have it because if we did, we'd be able to click on this and there should be a button up here somewhere.

Amol 27:34 Yeah, I think so too. OK. Let me email Jason.

Jayce C 27:52 I wonder if I could share these with you, but basically this is where I was attempting to do the salary planning, merit increase, and things like that. I can at least give you a starting point.

Amol 28:29 Yeah, seems like you snuck them in there while we still had access.

Jayce C 28:56 I think Bruce has it. Why don't I have the same capabilities as him? It's slowing me down.

Amol 29:58 OK, like a feeder model that corporate would control and they can just change it.

Jayce C 30:02 Yeah. The salary planning model is where I was building that functionality. In there I had amount, headcount, narrative, merit factor, burden factor, and some calculations. They could input one general amount or factor and then when we did the write process it would push it to every cost center in the target model.

Amol 31:13 OK, yeah, and that makes sense to me. That makes it easier and less messy.

Jayce C 31:32 There are multiple ways too. If we wanted to recalculate burden based on all of 2025 and push that to all of 2026, we can create a model that does that based off actuals, and then have a separate model that just controls the merit factor.

Jayce C 32:14 The stuff with the fan in front of it is the stuff that I created, like the SG&A reporting account and the SG&A cost center.

Amol 33:00 That gives me plenty to do at the start. I just need to mess around and figure out how to piece it all together.

Jayce C 33:32 I'll start doing some homework and get my mindset back into planning mode again.

Amol 34:03 This gives me plenty to start with. I'll definitely start messing around with the story. The data part is going to be a little confusing, but I'll try and mess around with that too.

Jayce C 34:21 OK, sounds good.

Amol 34:32 OK. All right. Talk to you later.

Jayce C 34:33 Alright, have a good one.

Amol 34:37 OK. Bye.

Amol stopped transcription
