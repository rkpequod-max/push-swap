/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "../libft/libft.h"
# include <unistd.h>
# include <stdlib.h>
# include <stdio.h>
# include <fcntl.h>

typedef struct		s_pile
{
	int				x;
	struct s_pile	*next;
}					t_pile;

typedef struct		s_x
{
	int				sizepa;
	int				sizepb;
}					t_x;

typedef struct		s_pivot
{
	int				min;
	int				max;
	int				op;
}					t_pivot;

int					pile_init(t_pile **p, char **nbs, int ac);
t_pile				*new_node(int x, t_pile *next);
void				print_pile(t_pile *p);
int					valid_input(int ac, char **strs);
int					islarger(char *nb);
void				other_side(t_pile **p1, t_pile **p2);
void				solve_it(t_pile **pa, t_pile **pb, int ispa, t_pivot v);
int					find_median(t_pile *head, int k);
int					median_between(t_pile *p, int min, int max);
int					count_between(t_pile *p, int min, int max);
void				mini_solve(t_pile **pa, t_pile **pb, int op);

void				pop(t_pile **head);
void				push(t_pile **head, int val);
int					sab(t_pile **p, char *str, int op);
int					pab(t_pile **p1, t_pile **p2, char *str, int op);
int					rab(t_pile **head, char *str, int op);
int					rrab(t_pile **head, char *str, int op);
int					are_left(t_pile *p, int pivot, int n, t_pivot v);
int					move_pivot(t_pile **p1, t_pile **p2, int ispa, t_pivot v);
int					last_between(t_pile *p, int min, int max);
void				quick_return(t_pile **p, t_pivot v);

void				free_pile(t_pile **p);
int					free_split(char **strs);
int					pile_len(t_pile *head);
int					is_swap(t_pile *p, int end);
t_pile				*end_node(t_pile *head);
int					first_half(t_pile **p1, t_pile **p2, int mov, int rev);
int					last_half(t_pile **p1, t_pile **p2, int mov, int rev);
void				pass_pile(t_pile **p1, t_pile **p2, int side);
int					ordered(t_pile *head, int ascendant);
int					closest_num(t_pile *p, int num);
int					pile_min(t_pile *p);
int					pile_max(t_pile *p);

#endif
