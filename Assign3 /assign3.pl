% Assignment 3 - Planning and Machine Learning written by
% Hanwen Shi, z5336691
% 19/04/2023

% Pick up coffee
action(	puc,
	state(cs,	false, SWC, MW, RHM),
	state(cs, true, SWC, MW, RHM)
).

% deliver coffee
action( dc,
	state(off, true, _, MW, RHM),
	state(off, false, false, MW, RHM)).

% pickup mail
action( pum,
	state(mr, RHC, SWC, true, false),
	state(mr, RHC, SWC, false, true)).

% deliver mail
action( dm,
	state(off, RHC, SWC, MW, true),
	state(off, RHC, SWC, MW, false)).

% Move clockwise
action(mc,
	state(CurrentLoc, RHC, SWC, MW, RHM),
	state(NextLoc, RHC, SWC, MW, RHM)) :-
	next(CurrentLoc, NextLoc).

% Move counter-clockwise
action(mcc,
			state(CurrentLoc, RHC, SWC, MW, RHM),
			state(PrevLoc, RHC, SWC, MW, RHM)) :-
    prev(CurrentLoc, PrevLoc).


next(cs, off).
next(off, lab).
next(lab, mr).
next(mr, cs).

% Define the previous location counter-clockwise
prev(cs, mr).
prev(mr, lab).
prev(lab, off).
prev(off, cs).

% plan(StartState, FinalState, Plan)

plan(State, State, []).				% To achieve State from State itself.

plan(State1, GoalState, [Action1 | RestofPlan]) :-
	action(Action1, State1, State2),		
	plan(State2, GoalState, RestofPlan). 		

id_plan(Start, Goal, Plan) :-
	append(Plan, _, _),
	plan(Start, Goal, Plan).




% Q2
:- op(300, xfx, <-).

% Inter-construction
inter_construction(C1 <- B1, C2 <- B2, C1 <- Z1B, C2 <- Z2B, C <- B) :-
  C1 \= C2,
  intersection(B1, B2, B),
  gensym(z, C),
  subtract(B1, B, B11),
  subtract(B2, B, B12),
  append(B11, [C], Z1B),
  append(B12, [C], Z2B).

% (q2.1) Intra-construction
intra_construction(C1 <- B1, C1 <- B2, C1 <- B11, C <- Z1B, C <- Z2B) :-
  intersection(B1, B2, B),
	reset_gensym,
  gensym(z, C),
  subtract(B1, B, Z1B),
  subtract(B2, B, Z2B),
  append(B, [C], B11).

% (q2.2) Absorption
absorption(C1 <- B1, C2 <- B2, C1 <- Z1B, C2 <- Z2B) :-
	subset(B1,B2) ->
		Z1B = B1,
		subtract(B2,B1,Rest),
		append(Rest,[C1],Z2B);
	subset(B2,B2) ->
		Z2B = B2,
		subtract(B1,B2,Rest),
		append(Rest,[C2],Z1B).

% (q2.3) Truncation
truncation(C1 <- B1, C1 <- B2, C1 <- B) :-
	intersection(B1,B2,B).
