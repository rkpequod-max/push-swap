/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   treatment.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_pile	*new_node(int x, t_pile *next)
{
	t_pile *new;

	if (!(new = (t_pile*)malloc(sizeof(t_pile))))
		return (NULL);
	new->x = x;
	new->next = next;
	return (new);
}

void	print_pile(t_pile *p)
{
	t_pile *current;

	current = p;
	ft_printf("\033[0;33m<head>[");
	while (current)
	{
		if (current->next)
			ft_printf("%d  ", current->x);
		else
			ft_printf("%d", current->x);
		current = current->next;
	}
	ft_printf("\033[0;33m]<end>\n\033[0m");
}

void	push(t_pile **head, int val)
{
	t_pile *new;

	new = new_node(val, *head);
	*head = new;
}

void	pop(t_pile **head)
{
	t_pile	*next_node;

	if (*head == NULL)
		return ;
	next_node = (*head)->next;
	free(*head);
	*head = next_node;
}

int		pile_init(t_pile **p, char **nbs, int ac)
{
	while (ac)
	{
		if (islarger(nbs[ac - 1]))
		{
			free_pile(p);
			return (0);
		}
		push(p, ft_atoi(nbs[--ac]));
	}
	return (1);
}
