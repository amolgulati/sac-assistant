# Overhead Planning Model Build Session

Source: `Overhead Planning Model Build Session.docx`

Date: April 10, 2026, 3:13 PM  
Duration: 1h 1m 1s

## Transcript

Gulati, Amol 0:03 to do some... What data transformation data transformation in the Excel file beforehand? I thought that maybe we could do it within SAC, but I think like, for example, the dates were in the wrong format. So I just had to kind of make it into this format rather than it was kind of like in the wrong format, essentially. So I did that within the file itself. Just want to confirm with you, is that kind of the way we should be doing it, or is there a way, or a more optimal way to do it within SAC, I guess it maybe doesn't matter, but...

Roundtree, Jayce C 0:52 Maybe just, we'll just instruct them that this is the format you have to enter the data in.

Gulati, Amol 0:59 Yeah, okay, that's what I figured, because it's a file, so we can just tell them, hey, this is the template. Okay, yeah, so I got... There's information in. Let me show you. Yeah, I got this job going. I don't know why it's giving me an orange. Oh, because there's four that were rejected.

Roundtree, Jayce C 1:28 And you can click on that download rejected drivers and that'll show you which ones it didn't load.

Gulati, Amol 1:49 Master Data. Ohh, no. No.

Roundtree, Jayce C 1:56 Yeah, like those two cleaned up.

Gulati, Amol 1:57 No, please.

Roundtree, Jayce C 2:03 The only thing I can point right there is the account is missing.

Gulati, Amol 2:04 Okay.

Roundtree, Jayce C 2:10 On 60100230. We got to check the account dimension and see if that account's in there. If not, then we need to add it.

Gulati, Amol 2:25 Mm. Okay, so this doesn't really give you any... inside here.

Roundtree, Jayce C 2:32 Yeah, I mean, it's basically telling you the reason it failed is because of the master data. It's just not telling me what the actual master data field is failing.

Gulati, Amol 2:39 Yeah. OK, sounds good.

Roundtree, Jayce C 2:44 But I would assume just because like those underscore nulls, those are going to be in there. That should be 000. And so we just need to see if that reporting account is in there, which I doubt it is, and if not, then we need to add it.

Gulati, Amol 3:06 Okay.

Roundtree, Jayce C 3:07 And you know, that's hopefully something that won't be an issue once we set up updating it all the time and all those kind of things.

Gulati, Amol 3:08 Yeah. Yeah. Yeah, for now it's probably okay just to kind of play around with it.

Roundtree, Jayce C 3:22 Yeah, yeah, if there's data in the model, you know, you at least have a base to mess around.

Gulati, Amol 3:23 Yeah. Yeah, yeah, okay. Okay, and so the other thing is... do I need to do anything with the burden increase and merit increase. I couldn't figure out how you did the calculation in there.

Gulati, Amol 4:36 Alright, so in here, I go to mapped effects. Merit increase, burden increase. Is there something that, like, is this the right way to do it in this?

Roundtree, Jayce C 4:50 I doubt you had that information in the text file, so technically what they would do is you would have a separate upload, an additional upload that just has the merit increase, and you could do it by period. And in the amount, because, you know, it's not really tied to profit center or an account or anything like that. You're just saying that this is what it is and you'll use the calculation to spread it amongst all the other accounts and whatnot.

Gulati, Amol 5:36 Yeah, about.

Roundtree, Jayce C 5:39 And then the burden increase, and for now we can... that one's a little different because we got to come up with a mechanism to calculate it, basically what the burden rate is from last year, by month, by cost center. But for now, you can just put like a flat rate in there.

Gulati, Amol 6:13 Okay, but I don't put that here. I put it in...

Roundtree, Jayce C 6:21 Yeah, so, so you cancel right here. And then go ahead and go to Excel and it'll create another CSV file.

Gulati, Amol 6:34 Okay.

Roundtree, Jayce C 7:11 And you can just have two columns and one for the period and one for increase. Then you just cut it in by September 2026 at one and then put it through 12.

Gulati, Amol 7:41 All right.

Roundtree, Jayce C 7:42 Well, you probably want to keep it in the same format.

Gulati, Amol 7:45 Yeah.

Roundtree, Jayce C 7:48 Should be able to just drag it down. I think it'll auto-fill.

Gulati, Amol 8:11 I was trying to get like all the months, but it's fine.

Roundtree, Jayce C 8:15 Yeah, well, I think you want to do that from 2026-01 to 2026-12. So we're trying to budget. We're doing the merit increase through December of 26.

Gulati, Amol 8:30 I see, I see, yeah, we're trying to do the future, that's right, so we don't need the past. Okay, that's right. OK.

Roundtree, Jayce C 8:38 Yeah. And then you would just type that for the first three months, so the one. Or no, it's going to be 100% because you don't want to have an increase. You want it to be the same.

Gulati, Amol 9:15 So this is where they can go in and they can just change it whatever they want to do.

Roundtree, Jayce C 9:20 Yeah.

Gulati, Amol 9:21 Yeah, OK.

Roundtree, Jayce C 10:11 Yeah. I don't know if you have to change that file type to a CSV, as of right now, it's all engineered, yeah.

Gulati, Amol 10:18 Yeah, that's what I'm doing. Give it to the CSV. OK, and then what about? Is there anything I need to do with the burden?

Roundtree, Jayce C 10:52 I mean, with the burden, you can technically...

Gulati, Amol 10:56 That's something separate. We're going to build something different for that.

Roundtree, Jayce C 11:00 Yeah, I mean, we basically, we could take, I think Alex had that included in her file. All the historical for 2025 is we could technically take that and calculate it ourselves for now, and then through a CSV do that by profit center, cost center, month.

Gulati, Amol 11:27 Absolutely.

Roundtree, Jayce C 11:27 And that wouldn't be a calculation, that will actually just be stored within the model. And then truly the only calculation you'll have on the model is the merit increase.

Gulati, Amol 11:38 Yeah. I guess it depends on if corporate wants to control it or if they want every user to be able to adjust it.

Roundtree, Jayce C 11:48 Yeah, I mean, the way we can do it is we can have it like an automated way. So as we say, you know, we're going to take last year's actuals and take those burden rates, and we're going to calculate them for you, and then you can have an adjustment line within the budget model to where if they want to tweak it and increase it a little bit or decrease it, they could. And the calculation within the budget model will combine the two members and then apply it to the salary.

Gulati, Amol 12:28 I think what we're trying to do is just have a pre-populate as much as we can, and then they go in there and tweak whatever they need.

Roundtree, Jayce C 12:52 Yeah, so did click that button.

Gulati, Amol 12:58 There.

Roundtree, Jayce C 12:58 Yeah.

Gulati, Amol 13:07 There we go. Yeah, this part takes forever just to get to that screen.

Roundtree, Jayce C 14:57 Okay, so it looks like it's not in percentage, so you may have to go to the CSV. And instead of using the percent format, just do like one and then 1.03.

Gulati, Amol 15:12 Okay. Yeah, that's probably what it is.

Roundtree, Jayce C 15:24 Okay, you can see that big T, little T, next to that merit increase, it was saying like reading out of the text.

Gulati, Amol 17:23 Yeah.

Roundtree, Jayce C 17:25 Can we change, like, hit the three dots over there and see if you can change the data type.

Gulati, Amol 18:37 Yeah, you can. Just trying to create transform, yeah, and then go here and you can change or replace.

Roundtree, Jayce C 18:53 Yeah, it's not gonna give you what you want.

Gulati, Amol 18:59 Might have to just change it, yeah, okay, that's fine.

Roundtree, Jayce C 19:05 I don't know why it's reading you as a text field.

Gulati, Amol 19:14 Yeah. It's weird.

Roundtree, Jayce C 19:24 Yeah, I agree.

Gulati, Amol 19:29 Alright, save. I'll try this one more time.

Roundtree, Jayce C 19:52 You start over because maybe it's holding on to something.

Gulati, Amol 19:57 Okay. Yeah. Yeah. That's true.

Roundtree, Jayce C 20:55 So now it looks like it's the number.

Gulati, Amol 20:58 Yeah, okay, so this looks better.

Roundtree, Jayce C 21:32 Yeah, I mean, it looks like it. I don't know the whole science that makes it look like it's a date format, but I'll just save and exit and run it.

Gulati, Amol 21:47 Yeah. Okay, so from here I have to go to the story.

Roundtree, Jayce C 22:12 Well, it's saying the configuration is not complete, so we have to click on the setup upload.

Gulati, Amol 22:28 Yeah, but... doesn't make any sense.

Roundtree, Jayce C 22:45 Can you make it a number instead of a string.

Gulati, Amol 22:56 There we go, yeah.

Roundtree, Jayce C 23:01 That's what I was looking for before. There's some easy way to change the format.

Gulati, Amol 23:43 Yeah. So, that's where I get confused - how do you run the upload job?

Roundtree, Jayce C 23:48 So that's where you got to go to the story and create the button.

Gulati, Amol 25:24 All right, so if I add...

Roundtree, Jayce C 25:45 They should go to that insert plus sign.

Gulati, Amol 25:50 Oh yeah, data action starter. Data upload starter.

Roundtree, Jayce C 25:55 Yeah.

Gulati, Amol 26:22 Salary planning, yeah, I think it's...

Roundtree, Jayce C 26:48 If you go to your model, it still said that it was not complete, so click on that. But all we need to do to get it set up.

Gulati, Amol 27:28 Yeah, when I click on set up upload, it doesn't do anything. This happened to me last time.

Roundtree, Jayce C 27:37 Go to click next. Are we going to review upload? We can do that because everything else appears to be done. Hit the drop-down, step through the tiles at the top.

Gulati, Amol 28:13 Save and exit. I don't see anything wrong here.

Roundtree, Jayce C 30:28 Go back to the mapping, and let's see something. On the account, hit the three dots on the very first line and set default value. Let me see if we have a merit account that is set up there to hold the value.

Gulati, Amol 31:11 Yeah. Oh, I see. Yeah. Because other ones have defaulted to pound sign.

Roundtree, Jayce C 31:12 Let me go to the dimensions. Type in merit increase. There you go. And for the profit center, just map it to the pound sign.

Gulati, Amol 32:31 Yeah, no issues found. Okay.

Roundtree, Jayce C 32:35 Now you're getting the option to finish.

Gulati, Amol 32:35 Yeah, that's the screen I got last time. Yeah, there we go.

Roundtree, Jayce C 33:19 I think once people start entering, that publish comes from because they start making changes, they have to publish it.

Gulati, Amol 35:19 But this is gonna cascade down all the way to all the accounts.

Roundtree, Jayce C 35:22 Yeah, once we do the calculation, we can tell it to make that amount persist amongst every profit center and cost center.

Gulati, Amol 35:37 Oh, yeah. Should I do that in structure or calculations?

Roundtree, Jayce C 35:53 Create an additional measure to hold that calc.

Gulati, Amol 36:23 Is this aggregation sum or does it matter?

Roundtree, Jayce C 36:26 Yeah, we can leave it there like that for now.

Gulati, Amol 36:56 Yeah. I'm going to measure.

Roundtree, Jayce C 37:02 Yeah. Call it something.

Gulati, Amol 37:35 Yeah. So.

Roundtree, Jayce C 37:42 Should be more than there called lookup.

Gulati, Amol 37:50 Okay. Oops. Alright, look up.

Roundtree, Jayce C 38:03 The first item we'll put in there is the measure, so it'd be the merit increase. Then in the second one, you're basically on your filters and your ignored dimensions. You could set the filter equal to the pound sign for profit center. And then your ignored dimensions will be after the comma and you'll do cost center.

Gulati, Amol 39:24 Yeah.

Roundtree, Jayce C 39:36 I think you should be able to see the additional fields.

Gulati, Amol 39:48 I don't think it's going down to each.

Roundtree, Jayce C 39:53 I don't see the additional fields. Hold on, look at that.

Gulati, Amol 40:26 Okay, yeah, I see.

Roundtree, Jayce C 40:35 If not, change your version to B1. Then click on it and it'll pop up.

Gulati, Amol 43:29 Alright, so no. I remember you showing me the screen, but I couldn't really understand what this was saying.

Roundtree, Jayce C 43:42 Yeah, so what you had to the left was what you filtered. So now you need to add on the rows profit center and flatten it.

Gulati, Amol 44:53 Filters, beyond measures. Oh, I'm missing that.

Roundtree, Jayce C 45:00 On the account filter just for the merit increase.

Gulati, Amol 45:42 Is this calc? Is this a formula right?

Roundtree, Jayce C 45:45 Okay. No, that's what I'm looking at. So get rid of where we have cost center equal to cost center. Get rid of that and keep the commas. Then after cost center, type in and do the profit center.

Gulati, Amol 47:18 Yeah. Yeah, I see it now. It's adding up.

Roundtree, Jayce C 47:58 Yeah, well, it should be showing all the profit centers, all the cost centers. That's what it should be showing.

Gulati, Amol 50:56 Aggregation type sum. So I guess what are you seeing that's wrong here?

Roundtree, Jayce C 51:13 Right now, it's only showing the profit center as pound and the cost center as pound. We want it to show every profit center and cost center that's on the model, so the purpose is that they input the merit increase one time and it cascades throughout the entire model.

Gulati, Amol 52:53 My lookup formula is pulling merit increase, but the lookup table likely only has data at one dimension intersection, and SAC can't disaggregate it down to the other dimension members.

Roundtree, Jayce C 54:54 There may be something where we just remove the account from the model and just have a salary measure, a merit measure, and a burden measure, because we're going to map those to one individual account anyway.

Gulati, Amol 55:26 Yeah.

Roundtree, Jayce C 55:29 But it's weird because I did basically the same thing without the account dimension. If you could share this model with me, then I can tinker around with it and see if I can get something to work. You're doing everything I did except you have one additional dimension than I did.

Roundtree, Jayce C 56:06 Let me share my screen real quick, just to show you that you're not going crazy. This is my model where you can see I loaded it to the profit center cost center. Here's my 1.03. And then this is my calculation saying take the merit increase and ignore the cost center and profit center that it was loaded to.

Gulati, Amol 56:59 Yeah.

Roundtree, Jayce C 57:02 So that's why I would just need to sit here and play with this until it works.

Gulati, Amol 57:10 How does your merit increase file look? Same thing.

Roundtree, Jayce C 57:17 Yeah, it just had a date and an amount. I didn't have a profit center, I didn't have a cost center or anything like that.

Gulati, Amol 59:09 So I have a merit increase calc in my measure. You don't have one. Maybe is that messing things up?

Roundtree, Jayce C 59:18 No, it shouldn't be messing things up because your calculation is not referencing it.

Gulati, Amol 59:53 Wonder if it's those four errors I got? Now, I don't think so.

Roundtree, Jayce C 1:00:05 Yeah, if you can share it with me, I can go in there and tinker with the lookup function.

Gulati, Amol 1:00:17 Yeah, I can do this.

Roundtree, Jayce C 1:00:35 It should be fine. I think I can go in there and tinker with it. It just won't allow it to save.

Gulati, Amol 1:00:46 I will do that. I appreciate it. At least I got past one hurdle.

Roundtree, Jayce C 1:00:52 Yeah, sounds good.

Gulati, Amol 1:00:54 Okay, all right. Sounds good. See ya.

Roundtree, Jayce C 1:00:57 We'll go again.

Gulati, Amol 1:00:58 You too. Bye.

Gulati, Amol stopped transcription
